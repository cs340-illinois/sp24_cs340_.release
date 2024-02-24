import threading

class Wallet:
  def __init__(self):
    """Initialize an empty wallet."""

  def get(self, resource):
    """Returns the amount of a given `resource` in this wallet."""

  def change(self, resource, delta):
    """
    Modifies the amount of a given `resource` in this wallet by `delta`.
    - If `delta` is negative, this function MUST NOT RETURN until the resource can be satisfied.
      (This function MUST BLOCK until the wallet has enough resources to satisfy the request.)
    - Returns the amount of resources in the wallet AFTER the change has been applied.
    """

  def try_change(self, resource, delta):
    """
    Like change, but if change would block
    this method instead leaves the resource unchanged and returns False.
    """

  def transaction(self, **delta):
    """
    Like calling change(key, value) for each key:value in `delta`, except:
    - All changes are made at once. If any change would block, the entire transaction blocks.
      Only continues once *all* the changes can be made as one atomic action.
    - Returns a dict of {resource:new_value} for all resources in the transaction.
    """
