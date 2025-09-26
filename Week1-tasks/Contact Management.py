"""
Task: Build a Contact Management System.
Description: Develop a command-line contact management system using Python.
- Implement functionalities such as adding contacts, searching for contacts by name, and updating contact information.
- Ensure proper error handling and data validation.
- Implement a basic contact management system using dictionaries or lists to store contact information and simple file I/O for data persistence.
"""
import json
import os
import re

class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    return json.load(file)
            return {}
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading contacts: {e}")
            return {}

    def save_contacts(self):
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.contacts, file, indent=2)
            return True
        except IOError as e:
            print(f"Error saving contacts: {e}")
            return False

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        pattern = r'^\+?[\d\s\-\(\)]{10,15}$'
        return re.match(pattern, phone) is not None

    def add_contact(self):
        try:
            name = input("Enter contact name: ").strip()
            if not name:
                print("Name cannot be empty!")
                return

            normalized_name = name.lower()
            if normalized_name in self.contacts:
                print("Contact already exists!")
                return

            phone = input("Enter phone number: ").strip()
            if phone and not self.validate_phone(phone):
                print("Invalid phone number format!")
                return
            elif not phone:
                phone = "N/A"

            email = input("Enter email address: ").strip()
            if email and not self.validate_email(email):
                print("Invalid email format!")
                return
            elif not email:
                email = "N/A"

            address = input("Enter address (optional): ").strip()
            if not address:
                address = "N/A"

            self.contacts[normalized_name] = {
                "original_name": name,
                "phone": phone,
                "email": email,
                "address": address
            }

            if self.save_contacts():
                print(f"Contact '{name}' added successfully!")
            else:
                print("Failed to save contact!")

        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def search_contact(self):
        try:
            search_term = input("Enter name to search: ").strip().lower()
            if not search_term:
                print("Search term cannot be empty!")
                return

            found_contacts = []
            for normalized_name, details in self.contacts.items():
                if search_term in normalized_name:
                    found_contacts.append(details)

            if found_contacts:
                print(f"\nFound {len(found_contacts)} contact(s):")
                for details in found_contacts:
                    self.display_contact(details)
            else:
                print("No contacts found!")

        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def update_contact(self):
        try:
            name = input("Enter contact name to update: ").strip()
            normalized_name = name.lower()

            if normalized_name not in self.contacts:
                print("Contact not found!")
                return

            current_details = self.contacts[normalized_name]
            print(f"\nCurrent details for '{current_details['original_name']}':")
            self.display_contact(current_details)

            print("\nEnter new details (press Enter to keep current value):")

            new_phone = input(f"Phone ({current_details['phone']}): ").strip()
            if new_phone and not self.validate_phone(new_phone):
                print("Invalid phone number format! Keeping current value.")
                new_phone = current_details['phone']
            elif not new_phone:
                new_phone = current_details['phone']

            new_email = input(f"Email ({current_details['email']}): ").strip()
            if new_email and not self.validate_email(new_email):
                print("Invalid email format! Keeping current value.")
                new_email = current_details['email']
            elif not new_email:
                new_email = current_details['email']

            new_address = input(f"Address ({current_details['address']}): ").strip()
            if not new_address:
                new_address = current_details['address']

            self.contacts[normalized_name] = {
                "original_name": current_details['original_name'],
                "phone": new_phone,
                "email": new_email,
                "address": new_address
            }

            if self.save_contacts():
                print(f"Contact '{current_details['original_name']}' updated successfully!")
            else:
                print("Failed to save updated contact!")

        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def delete_contact(self):
        try:
            name = input("Enter contact name to delete: ").strip()
            normalized_name = name.lower()

            if normalized_name not in self.contacts:
                print("Contact not found!")
                return

            confirm = input(f"Are you sure you want to delete '{self.contacts[normalized_name]['original_name']}'? (y/N): ").strip().lower()
            if confirm == 'y':
                del self.contacts[normalized_name]
                if self.save_contacts():
                    print(f"Contact '{name}' deleted successfully!")
                else:
                    print("Failed to save changes!")
            else:
                print("Deletion cancelled.")

        except KeyboardInterrupt:
            print("\nOperation cancelled.")

    def list_all_contacts(self):
        if not self.contacts:
            print("No contacts found!")
            return

        print(f"\nAll Contacts ({len(self.contacts)}):")
        for details in sorted(self.contacts.values(), key=lambda x: x['original_name'].lower()):
            self.display_contact(details)

    def display_contact(self, details):
        print(f"\n--- {details['original_name']} ---")
        print(f"Phone: {details.get('phone', 'N/A')}")
        print(f"Email: {details.get('email', 'N/A')}")
        print(f"Address: {details.get('address', 'N/A')}")

    def run(self):
        print("=== Contact Management System ===")

        while True:
            try:
                print("\nOptions:")
                print("1. Add Contact")
                print("2. Search Contact")
                print("3. Update Contact")
                print("4. Delete Contact")
                print("5. List All Contacts")
                print("6. Exit")

                choice = input("\nEnter your choice (1-6): ").strip()

                if choice == '1':
                    self.add_contact()
                elif choice == '2':
                    self.search_contact()
                elif choice == '3':
                    self.update_contact()
                elif choice == '4':
                    self.delete_contact()
                elif choice == '5':
                    self.list_all_contacts()
                elif choice == '6':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice! Please enter 1-6.")

            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    contact_manager = ContactManager()
    contact_manager.run()
