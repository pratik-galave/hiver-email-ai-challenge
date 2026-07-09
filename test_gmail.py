from gmail.gmail_client import get_service, fetch_unread_emails

service = get_service()

emails = fetch_unread_emails(service)

for email in emails:

    print("=" * 80)
    print("FROM:", email["from"])
    print("SUBJECT:", email["subject"])
    print()
    print(email["body"][:500])