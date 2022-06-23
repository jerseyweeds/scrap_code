Attribute VB_Name = "SenderPropertiesGet001"
Public Sub ZZZ_DomainGet()
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
        GetSenderDomain aObj
    Next
   
MsgBox "All Done getting properties"
   
End Sub

Public Sub GetSenderDomain(oMail As Object)

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




Dim Prop As UserProperty
If oMail.UserProperties.Count > 0 Then
    On Error Resume Next
    For Each Prop In oMail.UserProperties
        Debug.Print Prop.Name, oMail.SenderName, oMail.Subject
    Next
Else: Debug.Print "No properties found!", oMail.SenderName, oMail.Subject
End If


Err.Clear
Exit Sub
    
ErrorHandler:
    Debug.Print Err.Number & " - " & Err.Description
    Resume
    
End Sub


