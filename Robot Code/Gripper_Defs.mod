MODULE Gripper_Defs
    
    !*****************************************************
    !Module Name:   Gripper_Defs
    !Version:       1.0
    !Description:   Contains all definitions and procedures for grippers
    !Date Created:  25 May 2023
    !Date Updated:  -
    !Author:        Matthew DiMaggio
    !*****************************************************
    
    
    ! Digital Output Info:
    !   DO10_GripClose: Assigned to Board 10, Pin 1 (Index 0). Renamed from DO10_1.
    !   DO10_GripOpen: Assigned to Board 10, Pin 2 (Index 1). Renamed from DO10_2.
    
    
    ! Closes Gripper
    PROC CloseGripper()
        WaitRob\InPos;
        SetDO DO10_GripOpen, 0;
        SetDO DO10_GripClose, 1;
        WaitTime 0.3;
    ENDPROC
    
    ! Opens Gripper
    PROC OpenGripper()
        WaitRob\InPos;
        SetDO DO10_GripClose, 0;
        SetDO DO10_GripOpen, 1;
        WaitTime 0.3;
    ENDPROC

ENDMODULE