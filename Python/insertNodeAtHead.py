def insertNodeAtHead(head, data):
    # Write your code here
    if head is None:
        head = SinglyLinkedListNode(data)
        head.next = None
    elif head.next is None:
        head.next = SinglyLinkedListNode(head.data)
        head.data = data
    elif head.next.next is None:
        head.next.next = SinglyLinkedListNode(head.next.data)
        head.next.data = head.data
        head.data = data
    elif head.next.next.next is None:
        head.next.next.next = SinglyLinkedListNode(head.next.next.data)
        head.next.next.data = head.next.data
        head.next.data = head.data
        head.data = data
    else:
        head.next = insertNodeAtHead(head.next, head.data)
        head.data = data

    return head
