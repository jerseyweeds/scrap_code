Attribute VB_Name = "DedupeEmails001"
 Sub DeleteDuplicateEmailsInThisFolderForLoop()
    
 'zzz_clearDebugConsole
    
 Dim i, n, dupes As Long
 Dim updates, processed, deleted As Integer
 Dim Message, Item_ID, FolderStoreID, update_msg As String
 Dim StartTime, EndTime As Double
 Dim AppOL, NS, Folder As Object
 Dim target, Items As Object
 'Dim DELETE_LIST, EntryID_LIST, SenderList As New Scripting.Dictionary
 
 'Dim Items As Object
 'Dim Items As Scripting.dictionary
 'Dim DELETE_LIST As Scripting.dictionary
 
 StartTime = Timer
 
 dupes = 0
 deleted = 0
 
 'print updates every x records
 updates = 100

 Set Items = CreateObject("Scripting.Dictionary")
 Set DELETE_LIST = CreateObject("Scripting.Dictionary")
 Set EntryID_LIST = CreateObject("Scripting.Dictionary")
 Set SenderList = CreateObject("Scripting.Dictionary")
    
 'Initialize and instance of Outlook
 Set AppOL = CreateObject("Outlook.Application")
 'Get the MAPI Name Space
 Set NS = AppOL.GetNamespace("MAPI")
 'Use the current folder
 Set Folder = NS.Application.ActiveExplorer.CurrentFolder
 'Set Folder = NS.PickFolder 'OR Pick a folder
 FolderStoreID = Folder.StoreID

 Folder.Items.Sort "[SenderEmailAddress],[Subject],[SentOn]", False
 Set myItems = Folder.Items
 
 n = myItems.Count
 i = n
 processed = 0
 
 For Each item In myItems
    On Error Resume Next
    
    i = i - 1
    processed = processed + 1
    
    Message = item.SenderEmailAddress & "|" & item.Subject & "|" & item.SentOn
    Item_ID = item.EntryID
    
     'Check a dictionary variable for a match
    If Items.Exists(Message) = True Then
        dupes = dupes + 1
        DELETE_LIST.Add Item_ID, True
        'Debug.Print "ADDING: " & Item_ID
        
    Else
        Items.Add Message, True
        
    End If

    If i Mod updates = 0 Then
        DoEvents
        EndTime = Timer
        Debug.Print "Processing: " & i & " (" & CInt(((processed) / n) * 100) & "% DONE) " & _
                        dupes & " duplicates found. " & _
                        processed & " processed. " & _
                        Int(EndTime - StartTime) & " seconds elapsed. " & _
                        Int(processed / (EndTime - StartTime)) & " rec/sec. " & _
                        "ETA: " & Int((i / (processed / (EndTime - StartTime))) / 60) & " minutes."
    End If
    
    
 
 Next item
 
 'report back done reading
 EndTime = Timer
 Debug.Print "Processing: " & i & " (" & CInt(((processed) / n) * 100) & "% DONE) " & _
                dupes & " duplicates found. " & _
                processed & " processed. " & _
                Int(EndTime - StartTime) & " seconds elapsed. " & _
                Int(processed / (EndTime - StartTime)) & " rec/sec. " & _
                "ETA: " & Int((i / (processed / (EndTime - StartTime))) / 60) & " minutes."
             
 Debug.Print vbNewLine & processed & " items processed. " & _
             dupes & " duplicates. " & _
             "Execution time in seconds: " & EndTime - StartTime & vbNewLine
 
 
 Debug.Print "To be deleted: " & EntryID_LIST.Count
 
 For Each EntryID In DELETE_LIST.Keys
    deleted = deleted + 1
    'Set target = NS.GetItemFromID(EntryID, FolderStoreID)
    'target.Delete
    NS.GetItemFromID(EntryID, FolderStoreID).Delete
    If deleted Mod updates = 0 Then
       DoEvents
       Debug.Print "Deleted: " & deleted & " of " & dupes
    End If
 Next EntryID
 


ExitSub:

 EndTime = Timer
 
 'report back done deleting
 Debug.Print "Deleted: " & deleted & " of " & dupes
 Debug.Print vbNewLine & processed & " items processed. " & _
             dupes & " duplicates. " & _
             "Execution time in seconds: " & EndTime - StartTime & vbNewLine
    
 'Release the object variables from memory
 Set Folder = Nothing
 Set NS = Nothing
 Set AppOL = Nothing
 Set Folder = Nothing
 Set Items = Nothing
 Set target = Nothing
 Set DELETE_LIST = Nothing
 Set EntryID_LIST = Nothing
 Set SenderList = Nothing


 
 'MsgBox "Done!"
    
 End Sub
 
Sub zzz_clearDebugConsole()
    For i = 0 To 100
        Debug.Print ""
    Next i
End Sub

