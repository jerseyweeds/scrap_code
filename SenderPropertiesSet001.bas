Attribute VB_Name = "SenderPropertiesSet001"
Public Sub ZZZ_DomainSet_FromSelection()
  Call DomainSetFromSelection
End Sub

Public Sub ZZZ_DomainSet_FromSearchFolders()
  Call DomainSetFromSearchFolders
End Sub

Public Sub DomainSetSender(oMail As Object) 'Sub to set the Domain, YYYYMM, and YYYYMMDD

Dim oOutlook As Object    'Outlook.Application
Dim oProp As UserProperty
Dim itemtype, sDomain, sender, received_yyyymmdd, received_yyyymm
Dim i, max_i As Integer

On Error Resume Next
Set oOutlook = GetObject(, "Outlook.Application")           'Bind to existing instance of Outlook
If Err.Number <> 0 Then                                     'Could not get instance, so create a new one
   Err.Clear
   Set oOutlook = CreateObject("Outlook.Application")
End If


On Error Resume Next
sender = oMail.SenderEmailAddress
received_yyyymmdd = Format(oMail.ReceivedTime, "YYYY-MM-DD")
received_yyyymm = Format(oMail.ReceivedTime, "YYYY-MM")
sDomain = LCase(Right(oMail.SenderEmailAddress, Len(oMail.SenderEmailAddress) - InStr(1, oMail.SenderEmailAddress, "@")))


If InStr(sDomain, "exchange administrative group") <> 0 Then
    sDomain = "* no domain *"
End If

'MsgBox sDomain
Debug.Print "Domain: " & sDomain, "Sender: " & sender
On Error GoTo ErrorHandler

Set oProp1 = oMail.UserProperties.Add("Domain", olText, True)
    oProp1.Value = sDomain
Set oProp2 = oMail.UserProperties.Add("Received YYYY-MM-DD", olText, True)
    oProp2.Value = received_yyyymmdd
Set oProp3 = oMail.UserProperties.Add("Received YYYY-MM", olText, True)
    oProp3.Value = received_yyyymm

oMail.Save
Err.Clear
Exit Sub
    
ErrorHandler:
    Debug.Print Err.Number & " - " & Err.Description
    Resume
    
End Sub

Public Sub DomainSetFromSelection(Optional noop As Integer)

Dim oOutlook As Object    'Outlook.Application
Dim objSelection As Selection
Dim aObj As Object
Dim item As Object

i = 0

On Error Resume Next

Set oOutlook = GetObject(, "Outlook.Application")           'Bind to existing instance of Outlook
If Err.Number <> 0 Then                                     'Could not get instance, so create a new one
   Err.Clear
   Set oOutlook = CreateObject("Outlook.Application")
End If

On Error Resume Next
Set objSelection = Application.ActiveExplorer.Selection

For Each item In objSelection 'j = objSelection.Count To 1 Step -1
    'Set aObj = objSelection(j)
    i = i + 1
    If i Mod 10 = 0 Then
        DoEvents
        End If
    DomainSetSender item 'aObj
    Next
   
End Sub

Public Sub DomainSetFromSearchFolders()

Dim oOutlook As Object    'Outlook.Application
Dim oStores As Stores
Dim oStore As Store
Dim colStores As Stores
Dim oMail As Object
Dim i As Long
Dim itemtype As String
Dim aObj As Object
Dim oSearchFolders As Folders
Dim oFolder As Folder
Dim sSearchFolderName As String
Dim item As Object

sSearchFolderName = "No_user_fields_set"
i = 0
On Error Resume Next

Set oOutlook = GetObject(, "Outlook.Application")           'Bind to existing instance of Outlook
If Err.Number <> 0 Then                                     'Could not get instance, so create a new one
   Err.Clear
   Set oOutlook = CreateObject("Outlook.Application")
End If

Set colStores = Session.Stores
On Error Resume Next
'colStores // oStores
For Each oStore In colStores    'Debug.Print oStore.DisplayName, oStore.FilePath, oStore.Class
    Set oSearchFolders = oStore.GetSearchFolders
    On Error Resume Next
    For Each oFolder In oSearchFolders
        If StrComp(oFolder, sSearchFolderName) = 0 Then 'Debug.Print "Current folder: " & oFolder
            On Error Resume Next
            For Each item In oFolder.Items
                'Debug.Print Item.SenderEmailAddress
                i = i + 1
                If i Mod 10 = 0 Then
                    DoEvents
                    End If
                DomainSetSender item
                Next
            Exit Sub 'did what we needed now exiting...
            End If
        Next
    Next
    
End Sub
