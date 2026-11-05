# Services take a session and return models/tables, they never see request or http codes, call them from a route
# Get data through repositories, own the transaction, commit at the end of use.
# queue a task, send confirmation email (after commit)
# WORKER BEE