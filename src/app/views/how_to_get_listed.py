from django.views.generic.base import TemplateView

page_content = """
# How to get listed on ARKdelegates.io

## Step 1 - Register your delegate

Register a delegate on ARK mainnet. You can register a delegate within your ARK wallet.

## Step 2 - Find your delegate on ARKdelegates.io

We refresh a list of our delegates once per hour, so it can happen that you won't be able to immediately find your delegate, especially if registered it less than 1 hour ago.

Once you find your delegate (you can use the search form on the top of every page) click on it.

## Step 3 - Claim your account

On your delegates page, you'll be able to find a big red box which indicates an account hasn't been claimed. Claim it by clicking on the "Claim this account" link. A form will open - follow the instructions on that page.


## Experiencing issues?

In case of any issues, please join [ARK's Slack](https://ark.io/slack){target="_blank"} and ask in **#delegates** channel.

"""  # noqa


class HowToGetListed(TemplateView):
    template_name = 'how_to_get_listed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'seo': {
                'title': 'How to get listed on ARKdelegates.io',
                'description': (
                    'How to list your delegate on ARKdelegates.io and make your proposal publicly'
                )
            },
            'page_content': page_content.strip()
        })

        return context
