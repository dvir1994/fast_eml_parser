my_dict = [
("039266721", "John Doe"),
("039266721", "Sarah Doe"),
("039266721", "Johnny Doe"),
("307084285", "Mark Doe"),
]


def remove_duplicates(my_dict):

  seen = set()
  new_list = []
  for item in my_dict:
    if item[0] not in seen:
      seen.add(item[0])
      new_list.append(item)
  return new_list

unique_client_list = remove_duplicates(my_dict)
