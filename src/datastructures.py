class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = []
        self.next_id = 1  # Iniciar el ID desde 1

    def add_member(self, member):
        self.members.append(member)

    def get_member(self, member_id):
        return next((member for member in self.members if member["id"] == member_id), None)

    def get_all_members(self):
        return self.members

    def delete_member(self, member_id):
        member = self.get_member(member_id)
        if member:
            self.members.remove(member)
            return True
        return False

    def get_next_id(self):
        current_id = self.next_id
        self.next_id += 1
        return current_id
