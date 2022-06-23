Attribute VB_Name = "Testing001"
Sub RecursivelyGetFolders()

    Debug.Print "Running RecursivelyGetFolders"

    Dim OutApp As Outlook.Application
    Dim Namespace As Outlook.Namespace
    Dim Mfolder As Outlook.MAPIFolder
    Dim myMail As Outlook.Items
    
    Dim Folder As Outlook.MAPIFolder
    Dim SubFolder As Outlook.MAPIFolder
    Dim UserFolder As Outlook.MAPIFolder
    
    Set OutApp = New Outlook.Application
    Set Namespace = OutApp.GetNamespace("MAPI")
    Set Inbox = Namespace.GetDefaultFolder(olFolderInbox)
    
    ''Scan subfolder recursively
    ''https://stackoverflow.com/questions/45346183/excel-vba-looping-through-all-subfolders-in-outlook-email-to-find-an-email-with
    Set Namespace = OutApp.GetNamespace("MAPI")
    
    On Error Resume Next
    For Each Folder In Namespace.Folders
        For Each SubFolder In Folder.Folders
            For Each UserFolder In SubFolder.Folders
                Debug.Print Folder.Name, "|", SubFolder.Name, "|", UserFolder.Name
            Next UserFolder
        Next SubFolder
    Next Folder
    On Error GoTo 0
    
    
    'On Error Resume Next
    'For Each Item In Inbox.Items
    '    Debug.Print "INBOX", "|", Item.Subject
    'Next Item
    'On Error GoTo 0
    '
    'On Error Resume Next
    'For Each Folder In Inbox.Folders
    '    For Each Item In Folder.Items
    '            Debug.Print Folder.Name, "|", Item.Subject
    '    Next Item
    'Next Folder
    'On Error GoTo 0
    Debug.Print "================"
    Debug.Print "--- Finished ---"
    Debug.Print "================"


End Sub



Sub FindYourStore()
    Dim colStores As Outlook.Stores
    Dim oStore As Outlook.Store

    On Error Resume Next
    Set colStores = Application.Session.Stores
'You may use Session.Stores as shortcut
        For Each oStore In colStores
            Debug.Print oStore.DisplayName
        Next
End Sub


Sub ListSubjectLinesOfEmailsInASearchFolder()
    Dim StoreName As String
    Dim FolderName As String
    StoreName = "first.last@company.com"
    FolderName = "No_user_fields_set"
    Dim colStores As Outlook.Stores
    Dim oStore As Outlook.Store
    Dim oSearchFolders As Outlook.Folders
    Dim oFolder As Outlook.Folder
    Dim mail As Outlook.MailItem

    On Error Resume Next
    Set oFolder = Session.Stores.item(StoreName).GetSearchFolders(FolderName)
        For Each mail In oFolder.Items
            Debug.Print mail.Subject
        Next
End Sub



Sub FindYourStore2()

    Dim colStores As Outlook.Stores
    Dim oStore As Outlook.Store
    Dim oFolder As Outlook.Folder
    Dim StoreName As String
    Dim FolderName As String
    Dim FolderList As String
    
    Set oFolder = Application.Session.PickFolder
    StoreName = oFolder.Name
    
    FolderList = ""
    
    On Error Resume Next
    Set colStores = Application.Session.Stores
    For Each oStore In colStores
    If oStore.DisplayName = StoreName Then
    Set oSearchFolders = oStore.GetSearchFolders
    For Each oFolder In oSearchFolders
    ' Debug.Print (oFolder.FolderPath)
    FolderList = oFolder.Name & Chr(10) & FolderList
    Next
    End If
    Next
    
    FolderName = InputBox("Enter the search folder from the list:" & Chr(10) & FolderList)
    ListSubjectLinesOfEmailsInASearchFolder StoreName, FolderName

End Sub

