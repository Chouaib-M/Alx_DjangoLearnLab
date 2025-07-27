# Bookshelf Permissions and Groups

## Custom Permissions

- can_view:   Allows viewing books
- can_create: Allows creating new books
- can_edit:   Allows editing existing books
- can_delete: Allows deleting books

## Groups

- Viewers: Assign can_view
- Editors: Assign can_view, can_create, can_edit
- Admins:  Assign all permissions

Assign users to these groups via the Django admin interface.

Views are protected with @permission_required decorators. 