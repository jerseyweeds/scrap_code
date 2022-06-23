Attribute VB_Name = "MoveEmails001"
Sub MoveItemsToNewFolderForLoop()

    Dim objNamespace As Outlook.Namespace
    Dim sourceFolder As Outlook.MAPIFolder
    Dim destinationFolder As Outlook.MAPIFolder
    Dim Items As Outlook.Items
    Dim item As Object
    Dim Msg As String
    Dim i As Long, n As Long
    Dim StartTime As Double, EndTime As Double
    
    StartTime = Timer
    
    Set objNamespace = GetNamespace("MAPI")
    Set sourceFolder = objNamespace.Application.ActiveExplorer.CurrentFolder
    Set destinationFolder = objNamespace.PickFolder
    Set Items = sourceFolder.Items
    
    n = sourceFolder.Items.Count

    'Move emails in sourceFolder to destinationFolder
    Msg = n & " Items in " & sourceFolder.Name & ", Move?"

    If MsgBox(Msg, vbYesNo) = vbYes Then
        For Each item In Items
            'Debug.Print "Running: " & i & " on " & Items.Item(i).ConversationIndex
            'Set Item = Items.Item(i)
            DoEvents
            item.Move destinationFolder
            'Item.Move destinationFolder
        Next
        
    End If

    EndTime = Timer

    Debug.Print vbNewLine & "Execution time in seconds: ", EndTime - StartTime
    
ExitSub:
    
 'Release the object variables from memory
 Set sourceFolder = Nothing
 Set destinationFolder = Nothing
 Set objNamespace = Nothing
 Set Items = Nothing

End Sub



