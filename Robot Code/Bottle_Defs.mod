MODULE Bottle_Defs
    
    !*****************************************************
    !Module Name:   Bottle_Defs
    !Version:       1.0
    !Description:   Contains all procedures for picking up and placing a bottle
    !Date Created:  30 May 2023
    !Date Updated:  -
    !Author:        Matthew DiMaggio
    !*****************************************************
    
    VAR num MinX := 300;
    VAR num MaxX := 833;
    VAR num MinY := -2010;
    VAR num MaxY := -1670;
    
    PERS wobjdata BottleCurrent := [FALSE, TRUE, "", [[0, 0, 0], [1, 0, 0, 0]], [[488.503, -1973.31, 744], [1, 0, 0, 0]]];
    PERS wobjdata BottleNext := [FALSE, TRUE, "", [[0, 0, 0], [1, 0, 0, 0]], [[488.503, -1973.31, 744], [1, 0, 0, 0]]];
    
    PROC BottleLoop()
        PickupBottle;
        NextBottleLoc;
        DropoffBottle;
        UpdateBottlePos;
    ENDPROC
    
    PROC PickupBottle()
        WaitRob\InPos;
        MoveJ [[0, 0, 150], [0.5, 0.5, 0.5, -0.5], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v1000, z0, BulbGripper\WObj:=BottleCurrent;
        MoveL [[0, 0, 0], [0.5, 0.5, 0.5, -0.5], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v600, z0, BulbGripper\WObj:=BottleCurrent;
        WaitRob\InPos;
        CloseGripper;
        MoveL [[0, 0, 150], [0.5, 0.5, 0.5, -0.5], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v600, z0, BulbGripper\WObj:=BottleCurrent;
        WaitRob\InPos;
    ENDPROC
    
    PROC DropoffBottle()
        WaitRob\InPos;
        MoveJ [[0, 0, 150], [0.5, 0.5, 0.5, -0.5], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v1000, z0, BulbGripper\WObj:=BottleNext;
        MoveL [[0, 0, 0], [0.5, 0.5, 0.5, -0.5], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v600, z0, BulbGripper\WObj:=BottleNext;
        WaitRob\InPos;
        OpenGripper;
        MoveL [[0, 0, 150], [0.5, 0.5, 0.5, -0.5], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v600, z0, BulbGripper\WObj:=BottleNext;
        WaitRob\InPos;
    ENDPROC
    
    PROC NextBottleLoc()
        BottleNext.oframe.trans.X := rand(\min:=MinX,\max:=MaxX);
        BottleNext.oframe.trans.Y := rand(\min:=MinY,\max:=MaxY);
        
    ENDPROC
    
    PROC UpdateBottlePos()
        BottleCurrent.oframe.trans.X := BottleNext.oframe.trans.X;
        BottleCurrent.oframe.trans.Y := BottleNext.oframe.trans.Y;
    ENDPROC


ENDMODULE

