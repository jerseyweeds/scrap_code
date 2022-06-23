Attribute VB_Name = "Generic001"
Public Sub EnumerateFolders(ByVal oStartFolder As Object)
    'Modified from: https://docs.microsoft.com/en-us/office/vba/api/outlook.stores
    Dim oFolders               As Object 'Outlook.folders
    Dim oFolder                As Object 'Outlook.Folder
 
    On Error Resume Next
 
    Set oFolders = oStartFolder.Folders
 
    If oFolders.Count > 0 Then
        For Each oFolder In oFolders
            Debug.Print , oFolder.Name, oFolder.FolderPath, oFolder.Class
            Call EnumerateFolders(oFolder)
        Next
    End If
 
    If Not oFolder Is Nothing Then Set oFolder = Nothing
    If Not oFolders Is Nothing Then Set oFolders = Nothing
End Sub

