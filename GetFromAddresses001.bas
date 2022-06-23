Attribute VB_Name = "GetFromAddresses001"

Public Sub ZZZ_AddressesCopyFromSelectionGet()

' ***        IMPORTANT         ***
'
' !!! DO NOT DELETE THIS MACRO !!!
'
' ***        IMPORTANT         ***

'get the sender email addresses from the selected messages

Debug.Print "Running GetFromAddressesFromSelection"

Dim oOutlook As Object    'Outlook.Application
On Error Resume Next
Set oOutlook = GetObject(, "Outlook.Application")           'Bind to existing instance of Outlook
If Err.Number <> 0 Then                                     'Could not get instance, so create a new one
   Err.Clear
   Set oOutlook = CreateObject("Outlook.Application")
End If

Dim objSelection As Selection
Dim aObj As Object
Dim oMail As MailItem
Dim sender As String
Dim final_list As String

Set objSelection = Application.ActiveExplorer.Selection
Set sender_list = CreateObject("System.Collections.ArrayList")

On Error Resume Next
    For Each aObj In objSelection
        If TypeName(aObj) = "MailItem" Then
            
            sender = aObj.SenderEmailAddress
            
            If sender_list.contains(sender & "; ") Then
                Debug.Print "Skipping: " & sender & " (already exists)"
            Else
                sender_list.Add sender & "; "
            End If

            Debug.Print "Adding:   " & sender
        End If
    Next

Dim Name As Variant
For Each Name In sender_list
    final_list = final_list & Name
Next
     
Debug.Print final_list

InputBox "Here is a distinct list of the senders for the emails selected...", "Copy Text", final_list

End Sub


