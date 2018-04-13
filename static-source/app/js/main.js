$(document).foundation();

if (document.querySelector('input[name="csrfmiddlewaretoken"')) {
    var csrfmiddlewaretoken = document.querySelector('input[name="csrfmiddlewaretoken"').value;
} else {
    var csrfmiddlewaretoken = '';
}

$('[data-toggle]').on('click', function () {
    var type = $(this).data('type');
    var action = $(this).data('action');

    switch (type) {
        case 'contribution':
            if (action === 'edit') {
                var contributionId = $(this).data('id');
                editContribution(contributionId);
            } else if (action == 'create') {
                triggerCreateContribution();
            } else if (action == 'delete') {
                var contributionId = $(this).data('id');
                deleteContribution(contributionId);
            } else {
                throw Error('Unknown action');
            }
            break;

        case 'node':
            if (action === 'edit') {
                var nodeId = $(this).data('id');
                editNode(nodeId);
            } else if (action == 'create') {
                triggerCreateNode();
            } else if (action == 'delete') {
                var nodeId = $(this).data('id');
                deleteNode(nodeId);
            } else {
                throw Error('Unknown action');
            }
            break;

        case 'proposal':
            if (action === 'edit') {
                editProposal();
            } else {
                throw Error('Unknown action');
            }
            break;
        default:
            console.log('do nothing yo');
    }
});

/**
 * Contribution
 */
function editContribution(contributionId) {
    var actionUrl = '/edit/contribution/?id=' + contributionId;
    $.ajax({
        url: actionUrl,
        dataType: 'json',
        contentType: 'application/json',
        xhrFields: {
            withCredentials: true
        }
    })
    .done(function (data) {
        var form = document.querySelector('#editCreateContributionForm');
        var titleEl = form.querySelector('input[name="title"]');
        var descriptionEl = form.querySelector('textarea[name="description"]');

        titleEl.value = data.title;
        descriptionEl.value = data.description;
        form.action = actionUrl;

        initFormSubmitListener(form, saveContribution);
    });
}

function saveContribution(form) {
    var actionUrl = form.action;
    var titleEl = form.querySelector('input[name="title"]');
    var descriptionEl = form.querySelector('textarea[name="description"]');

    $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
        jqXHR.setRequestHeader('X-CSRFToken', csrfmiddlewaretoken);
    });
    $.ajax({
        method: 'PUT',
        url: actionUrl,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({title: titleEl.value, description: descriptionEl.value}),
        xhrFields: {
            withCredentials: true
        }
    })
    .done(function(data) {
        $('#editCreateContribution').foundation('close');
        window.location.reload(true);
    })
    .fail(function(error) {
        alert('There was an error updating a contribution.');
        console.log('There was an error updating a contribution:', error);
    });
};

function triggerCreateContribution() {
    var form = document.querySelector('#editCreateContributionForm');
    initFormSubmitListener(form, createContribution);
}

function createContribution(form) {
    var actionUrl = form.action;
    var titleEl = form.querySelector('input[name="title"]');
    var descriptionEl = form.querySelector('textarea[name="description"]');
    $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
        jqXHR.setRequestHeader('X-CSRFToken', csrfmiddlewaretoken);
    });
    $.ajax({
        method: 'POST',
        url: actionUrl,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({title: titleEl.value, description: descriptionEl.value}),
        xhrFields: {
            withCredentials: true
        }
    })
    .done(function(data) {
        $('#editCreateContribution').foundation('close');
        window.location.reload(true);
    })
    .fail(function(error) {
        alert('There was an error creating a contribution.');
        console.log('There was an error creating a contribution:', error);
    });
}

function deleteContribution(contributionId) {
    var form = document.querySelector('#deleteContribution');
    var actionUrl = '/edit/contribution/?id=' + contributionId;
    var deleteYes = form.querySelector('.delete-yes');
    var deleteNo = form.querySelector('.delete-no');

    $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
        jqXHR.setRequestHeader('X-CSRFToken', csrfmiddlewaretoken);
    });

    deleteYes.addEventListener('click', function (e) {
        e.preventDefault();
        $.ajax({
            method: 'DELETE',
            url: actionUrl,
            dataType: 'json',
            contentType: 'application/json',
            xhrFields: {
                withCredentials: true
            }
        })
        .done(function( data ) {
            $('#deleteContribution').foundation('close');
            window.location.reload(true);
        })
        .fail(function(error) {
            alert('There was an error deleting a contribution.');
            console.log('There was an error deleting a contribution:', error);
        });
    });

    deleteNo.addEventListener('click', function(e) {
        e.preventDefault();
        $('#deleteContribution').foundation('close');
    });
}


/**
 * Node
 */

function editNode(nodeId) {
    var actionUrl = '/edit/node/?id=' + nodeId;
    $.ajax({
        url: actionUrl,
        dataType: 'json',
        contentType: 'application/json',
        xhrFields: {
            withCredentials: true
        }
    })
    .done(function (data) {
        var form = document.querySelector('#editCreateNodeForm');

        var networkEl = form.querySelector('select[name="network"]');
        var cpuEl = form.querySelector('input[name="cpu"]');
        var memoryEl = form.querySelector('input[name="memory"]');
        var isDedicatedEl = form.querySelector('input[name="is_dedicated"]');
        var isBackupEl = form.querySelector('input[name="is_backup"]');
        networkEl.value = data.network;
        cpuEl.value = data.cpu;
        memoryEl.value = data.memory;
        isDedicatedEl.checked = data.is_dedicated;
        isBackupEl.checked = data.is_backup;

        form.action = actionUrl;

        initFormSubmitListener(form, saveNode);
    });
}

function saveNode(form) {
    var actionUrl = form.action;
    var networkEl = form.querySelector('select[name="network"]');
    var cpuEl = form.querySelector('input[name="cpu"]');
    var memoryEl = form.querySelector('input[name="memory"]');
    var isDedicatedEl = form.querySelector('input[name="is_dedicated"]');
    var isBackupEl = form.querySelector('input[name="is_backup"]');

    $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
        jqXHR.setRequestHeader('X-CSRFToken', csrfmiddlewaretoken);
    });
    $.ajax({
        method: 'PUT',
        url: actionUrl,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            network: networkEl.value,
            cpu: cpuEl.value,
            memory: memoryEl.value,
            is_dedicated: isDedicatedEl.checked,
            is_backup: isBackupEl.checked
        }),
        xhrFields: {
            withCredentials: true
        }
    })
    .done(function(data) {
        $('#editCreateContribution').foundation('close');
        window.location.reload(true);
    })
    .fail(function(error) {
        alert('There was an error updating a contribution.');
        console.log('There was an error updating a contribution:', error);
    });
};

function createNode(form) {
    var actionUrl = form.action;
    var networkEl = form.querySelector('select[name="network"]');
    var cpuEl = form.querySelector('input[name="cpu"]');
    var memoryEl = form.querySelector('input[name="memory"]');
    var isDedicatedEl = form.querySelector('input[name="is_dedicated"]');
    var isBackupEl = form.querySelector('input[name="is_backup"]');

    $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
        jqXHR.setRequestHeader('X-CSRFToken', csrfmiddlewaretoken);
    });
    $.ajax({
        method: 'POST',
        url: actionUrl,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            network: networkEl.value,
            cpu: cpuEl.value,
            memory: memoryEl.value,
            is_dedicated: isDedicatedEl.checked,
            is_backup: isBackupEl.checked
        }),
        xhrFields: {
            withCredentials: true
        }
    })
    .done(function(data) {
        $('#editCreateNode').foundation('close');
        window.location.reload(true);
    })
    .fail(function(error) {
        alert('There was an error creating a node.');
        console.log('There was an error creating a node:', error);
    });
}

function deleteNode(nodeId) {
    var form = document.querySelector('#deleteNode');
    var actionUrl = '/edit/node/?id=' + nodeId;
    var deleteYes = form.querySelector('.delete-yes');
    var deleteNo = form.querySelector('.delete-no');

    $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
        jqXHR.setRequestHeader('X-CSRFToken', csrfmiddlewaretoken);
    });

    deleteYes.addEventListener('click', function (e) {
        e.preventDefault();
        $.ajax({
            method: 'DELETE',
            url: actionUrl,
            dataType: 'json',
            contentType: 'application/json',
            xhrFields: {
                withCredentials: true
            }
        })
        .done(function( data ) {
            $('#deleteNode').foundation('close');
            window.location.reload(true);
        })
        .fail(function(error) {
            alert('There was an error deleting a node.');
            console.log('There was an error deleting a node:', error);
        }).always(function() {
            // remove event listener?
        });
    });

    deleteNo.addEventListener('click', function(e) {
        e.preventDefault();
        $('#deleteContribution').foundation('close');
    });
}

function triggerCreateNode() {
    var form = document.querySelector('#editCreateNodeForm');
    initFormSubmitListener(form, createNode);
}

/**
 * Proposal
 */
function editProposal() {
    var actionUrl = '/edit/proposal/';
    $.ajax({
        url: actionUrl,
        dataType: 'json',
        contentType: 'application/json',
        xhrFields: {
            withCredentials: true
        }
    })
    .done(function (data) {
        var form = document.querySelector('#editProposalForm');

        var proposalEl = form.querySelector('textarea[name="proposal"]');
        proposalEl.value = data.proposal;

        form.action = actionUrl;

        initFormSubmitListener(form, saveProposal);
    });
}

function saveProposal(form) {
    var actionUrl = form.action;
    var proposalEl = form.querySelector('textarea[name="proposal"]');

    $.ajaxPrefilter(function (options, originalOptions, jqXHR) {
        jqXHR.setRequestHeader('X-CSRFToken', csrfmiddlewaretoken);
    });
    $.ajax({
        method: 'PUT',
        url: actionUrl,
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
            proposal: proposalEl.value,
        }),
        xhrFields: {
            withCredentials: true
        }
    })
    .done(function(data) {
        $('#editCreateContribution').foundation('close');
        window.location.reload(true);
    })
    .fail(function(error) {
        alert('There was an error updating your proposal.');
        console.log('There was an error updating your proposal:', error);
    });
};

/**
 * Other
 */
function initFormSubmitListener(form, actionHandler) {
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        actionHandler(form);
        e.target.removeEventListener(e.type, arguments.callee);
    });
}
