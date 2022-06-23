Attribute VB_Name = "SenderPropertiesClear001"
Sub ZZZ_ClearDomain_Selection()
' ***        IMPORTANT         ***
'
' !!! DO NOT DELETE THIS MACRO !!!
'
' ***        IMPORTANT         ***


' Manually set the domain and YYYY-MM-DD from selected item in Outlook
    
Debug.Print "Running ClearSenderDomain"

Dim oOutlook As Object    'Outlook.Application
On Error Resume Next
Set oOutlook = GetObject(, "Outlook.Application")           'Bind to existing instance of Outlook
If Err.Number <> 0 Then                                     'Could not get instance, so create a new one
   Err.Clear
   Set oOutlook = CreateObject("Outlook.Application")
End If

Dim objSelection As Selection
Dim aObj As Object
On Error Resume Next
Set objSelection = Application.ActiveExplorer.Selection
    For Each aObj In objSelection
        ClearSenderDomain aObj
    Next
   
MsgBox "All Done clearing properties"
   
End Sub

Private Sub ClearSenderDomain(oMail As Object)

' ***        IMPORTANT         ***
'
' !!! DO NOT DELETE THIS MACRO !!!
'
' ***        IMPORTANT         ***
    
'Debug.Print "Running ClearSenderDomain"

Dim oOutlook As Object    'Outlook.Application
On Error Resume Next
Set oOutlook = GetObject(, "Outlook.Application")           'Bind to existing instance of Outlook
If Err.Number <> 0 Then                                     'Could not get instance, so create a new one
   Err.Clear
   Set oOutlook = CreateObject("Outlook.Application")
End If



On Error Resume Next

For j = oMail.UserProperties.Count To 1 Step -1
        Set Prop = oMail.UserProperties(j)
        'Debug.Print "Deleting", Prop.Name, oMail.SenderName, oMail.Subject
        Prop.Delete
    Next
    
oMail.Save



Err.Clear
Exit Sub
    
ErrorHandler:
    Debug.Print Err.Number & " - " & Err.Description
    Resume
    
End Sub

