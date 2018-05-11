"""
TODO: Optimize these two SQL queries
"""

sql_delegates = """
SELECT
    app_delegate.id,
    app_delegate.name,
    app_delegate.address,
    app_delegate.is_private,
    latest_history.*,
    node_coude.count as total_nodes_count,
    has_backup.count as backup_nodes_count,
    contributions.count as contributions_count
FROM
    app_delegate
INNER JOIN
(
    SELECT
        DISTINCT ON (app_history_delegate.delegate_id) delegate_id,
        app_history_delegate.history_id,
        app_history.voters,
        app_history.uptime,
        app_history.approval,
        app_history.rank,
        app_history.forged,
        app_history.missed,
        app_history.created,
        app_history.voting_power,
        app_history.payload->'voters_zero_balance' as voters_zero_balance,
        app_history.payload->'voters_not_zero_balance' as voters_not_zero_balance
    FROM
        app_history_delegate, app_history
    WHERE
        app_history_delegate.history_id = app_history.id
    ORDER BY app_history_delegate.delegate_id, app_history.created DESC
) as latest_history ON latest_history.delegate_id = app_delegate.id
LEFT OUTER JOIN
(
    SELECT count(id) as count, delegate_id FROM app_node WHERE is_active = True GROUP BY app_node.delegate_id
) as node_coude ON node_coude.delegate_id = app_delegate.id
LEFT OUTER JOIN
(
    SELECT count(id) as count, delegate_id FROM app_node WHERE is_active = True AND is_backup = True GROUP BY delegate_id
) as has_backup ON has_backup.delegate_id = app_delegate.id
LEFT OUTER JOIN
(
    SELECT count(id) as count, delegate_id FROM app_contribution GROUP BY delegate_id
) as contributions ON contributions.delegate_id = app_delegate.id
ORDER BY latest_history.rank ASC
"""


sql_select_all_info_for_delegate_via_slug = """
SELECT
    delegate.id,
    delegate.name,
    delegate.address,
    app_history.voters,
    app_history.uptime,
    app_history.approval,
    app_history.rank,
    app_history.forged,
    app_history.missed,
    app_history.created,
    app_history.voting_power,
    app_history.payload->'voters_zero_balance' as voters_zero_balance,
    app_history.payload->'voters_not_zero_balance' as voters_not_zero_balance,
    node_coude.count as total_nodes_count,
    has_backup.count as backup_nodes_count,
    contributions.count as contributions_count
FROM
    app_history
LEFT OUTER JOIN (
    SELECT *
    FROM app_history_delegate
    WHERE app_history_delegate.delegate_id = (SELECT id FROM app_delegate WHERE slug = %s)
) as delegate_history ON delegate_history.history_id = app_history.id
LEFT OUTER JOIN (
    SELECT *
    FROM app_delegate
    WHERE slug = %s
) as delegate ON delegate.id = delegate_history.delegate_id
LEFT OUTER JOIN
(
    SELECT count(id) as count, delegate_id FROM app_node WHERE is_active = True GROUP BY app_node.delegate_id
) as node_coude ON node_coude.delegate_id = delegate.id
LEFT OUTER JOIN
(
    SELECT count(id) as count, delegate_id FROM app_node WHERE is_active = True AND is_backup = True GROUP BY delegate_id
) as has_backup ON has_backup.delegate_id = delegate.id
LEFT OUTER JOIN
(
    SELECT count(id) as count, delegate_id FROM app_contribution GROUP BY delegate_id
) as contributions ON contributions.delegate_id = delegate.id
WHERE
    delegate_history.delegate_id = (SELECT id FROM app_delegate WHERE slug = %s)
ORDER BY app_history.created DESC
LIMIT 1
"""

sql_delegate_all_info_via_slug = """
SELECT
    delegate.*,
    app_history.voters,
    app_history.uptime,
    app_history.approval,
    app_history.rank,
    app_history.forged,
    app_history.missed,
    app_history.created,
    app_history.voting_power,
    app_history.payload->'voters_zero_balance' as voters_zero_balance,
    app_history.payload->'voters_not_zero_balance' as voters_not_zero_balance
FROM
    app_history
LEFT OUTER JOIN (
    SELECT *
    FROM app_history_delegate
    WHERE app_history_delegate.delegate_id = (SELECT id FROM app_delegate WHERE slug = %s)
) as delegate_history ON delegate_history.history_id = app_history.id
LEFT OUTER JOIN (
    SELECT *
    FROM app_delegate
    WHERE slug = %s
) as delegate ON delegate.id = delegate_history.delegate_id
WHERE
    delegate_history.delegate_id = (SELECT id FROM app_delegate WHERE slug = %s)
ORDER BY app_history.created DESC
LIMIT 1
"""
