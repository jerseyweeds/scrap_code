Attribute VB_Name = "Timer001"
Declare PtrSafe Function SetTimer Lib "user32" (ByVal hwnd As Long, ByVal nIDEvent As Long, ByVal uElapse As Long, ByVal lpTimerfunc As Long) As Long
Declare PtrSafe Function KillTimer Lib "user32" (ByVal hwnd As Long, ByVal nIDEvent As Long) As Long

Public TimerID As Long 'Need a timer ID to eventually turn off the timer. If the timer ID <> 0 then the timer is running

Public Sub TriggerTimer(ByVal hwnd As Long, ByVal uMsg As Long, ByVal idevent As Long, ByVal Systime As Long)
  'MsgBox "The TriggerTimer function has been automatically called!"
  Call ZZZ_DomainSet_FromSearchFolders
End Sub

Public Sub ZZZ_TimerDeactivate()
    DeactivateTimer
End Sub

Public Sub ZZZ_TimerActivate()
    ActivateTimer
End Sub

Public Sub ActivateTimer(Optional ByVal nMinutes As Long)
    
    If IsMissing(nMinutes) Then
        nMinutes = 5
    End If
        
    If nMinutes < 1 Then
        nMinutes = InputBox("Enter the number of minutes", "User Input", 5)
    End If
    
    Debug.Print "Activating timer ", nMinutes, "minutes"
    
    nMinutes = nMinutes * 1000 * 60 'The SetTimer call accepts milliseconds, so convert to minutes
    
    If TimerID <> 0 Then
        Call DeactivateTimer 'Check to see if timer is running before call to SetTimer
        TimerID = SetTimer(0, 0, nMinutes, AddressOf TriggerTimer)
        If TimerID = 0 Then
            'MsgBox "The timer failed to activate."
        End If
    End If
  
    Debug.Print "Activating timer", TimerID
  
End Sub

Public Sub DeactivateTimer()

    Debug.Print "Deactivating timer "

    Dim lSuccess As Long
    
    lSuccess = KillTimer(0, TimerID)
    
    If lSuccess = 0 Then
        'MsgBox "The timer failed to deactivate. "
    Else
        TimerID = 0
    End If
    
    Debug.Print "Deactivating timer ", lSuccess, TimerID
  
End Sub




