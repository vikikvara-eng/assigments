from functools import wraps

SYSTEM_ACTIVE = True
GLOBAL_AUDIT_LOG = []


def audit_system(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if SYSTEM_ACTIVE:
      GLOBAL_AUDIT_LOG.append(f"გამოძახებულია ფუნქცია: {func.__name__}")
    return func(*args, **kwargs)

  return wrapper


def create_account_generator(initial_balance):
  balance = initial_balance
  transaction_id = 0

  @audit_system
  def account_generator():
    nonlocal balance, transaction_id
    while True:
      amount = yield (transaction_id, balance)
      if amount is not None:
        balance += amount
        transaction_id += 1

  gen = account_generator()
  next(gen)
  return gen


if __name__ == "__main__":
  account = create_account_generator(1000)
  print(account.send(500))
  print(account.send(200))
  print("აუდიტ პირობები:", GLOBAL_AUDIT_LOG)