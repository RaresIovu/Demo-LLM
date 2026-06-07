New feature: Product filtering

Modify getAllKnowledge function in service.py so that it also returns the categories of the products.

In frontend, the page /products will now also contain a filtering option. Checkboxes for each category will appear, and checking them will show the list of products with those categories. It wont do a refetch, the product list is kept entirely, its just that user can choose to show only certain ones.

