from django.views.generic.base import TemplateView

faq_content = """
# ARK FAQ page

## What is ARK?
[Watch this video](https://www.youtube.com/watch?v=E0IRwe9Iv3w){target="_blank"}

## What is DPOS?
[Watch this video](https://www.youtube.com/watch?v=YT_xMwT8CnA&t){target="_blank"}

## How to use ARK wallet?
[Watch this video](https://www.youtube.com/watch?v=sO_blc3DEhk){target="_blank"}

## How does DPOS in ARK work?
[Read about it here.](https://blog.ark.io/dpos-and-ark-voting-explained-68596a171ca1){target="_blank"}

## Voting/unvoting an ARK delegate
- How to vote for an ARK delegate?
- How to unvote an ARK delegate?
- What is the cost of voting?
- Do I need to have my wallet open?

[Read about it here in more detail.](https://blog.ark.io/how-to-vote-or-un-vote-an-ark-delegate-and-how-does-it-all-work-819c5439da68){target="_blank"}

[How to vote for an ARK delegate (video)](https://www.youtube.com/watch?v=GJHhTA78QQQ){target="_blank"}

## How to get in touch with a delegate?

Join [ARK's Slack](https://ark.io/slack){target="_blank"} and ask in **#delegates** channel.

"""  # noqa


class FAQ(TemplateView):
    template_name = "faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "seo": {
                    "title": "ARK FAQ @ ARKdelegates.io",
                    "description": (
                        "Frequently asked questions about ARK delegates, DPO and ARK blockchain."
                    ),
                },
                "faq_content": faq_content.strip(),
            }
        )

        return context
