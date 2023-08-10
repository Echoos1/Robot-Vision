MODULE LightBulb_Defs
    
    !*****************************************************
    !Module Name:   Lightbulb_Defs
    !Version:       1.1
    !Description:   Contains all definitions and procedures for picking up and screwing in a lightbulb
    !Date Created:  25 May 2023
    !Date Updated:  1 June 2023
    !Author:        Matthew DiMaggio
    !*****************************************************
    
    VAR jointtarget ScrewPos0a;
    VAR jointtarget ScrewPos1;
    VAR jointtarget ScrewPos2;
    VAR jointtarget ScrewPos3;
    VAR jointtarget ScrewPos4;
    
    VAR bool check;
    VAR num pickupX;
    VAR num pickupY;
    VAR num dropoffX;
    VAR num dropoffY;
    VAR pos dropoffXYZ;
    VAR pos pickupXYZ;
    
    
    PROC Lightbulb_Full()
        MoveAbsJ ZeroPoint, v500, z0, BulbGripper\WObj:=wobj0;
        !randomize_pickup;
        !randomize_screwin;
        check := StrToVal(ValToStr(PickupWobj.oframe.trans.X),pickupX);
        check := StrToVal(ValToStr(PickupWobj.oframe.trans.Y),pickupY);
        check := StrToVal(ValToStr(DropoffWobj.oframe.trans.X),dropoffX);
        check := StrToVal(ValToStr(DropoffWobj.oframe.trans.Y),dropoffY);
        dropoffXYZ := [dropoffX,dropoffY,0];
        pickupXYZ := [pickupX,pickupY,0];
        
        ScrewPos_MovetoJoint;
        PickupBulb;
        ScrewInBulb;
        UnscrewBulb;
        PlacebulbBack;
    ENDPROC
    
    PROC ScrewPos_MovetoJoint()
        check_pos\XYZ:=dropoffXYZ;
        OpenGripper;
        
        MoveJ [[0, 0, -300], [1, 0, 0, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=DropoffWobj;
        WaitRob\InPos;
        ScrewPos0a := CJointT();
        
        MoveJ [[0, 0, -24.18], [1, 0, 0, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=DropoffWobj;
        WaitRob\InPos;
        ScrewPos1 := CJointT();
        
        MoveJ [[0, 0, -16.12], [1, 0, 0, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=DropoffWobj;
        WaitRob\InPos;
        ScrewPos2 := CJointT();
        
        MoveJ [[0, 0, -8.06], [1, 0, 0, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=DropoffWobj;
        WaitRob\InPos;
        ScrewPos3 := CJointT();
        
        MoveJ [[0, 0, 0], [1, 0, 0, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=DropoffWobj;
        WaitRob\InPos;
        ScrewPos4 := CJointT();
        
        MoveJ [[0, 0, -300], [1, 0, 0, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=DropoffWobj;
        check_pos\XYZ:=dropoffXYZ;
    ENDPROC
    
    PROC PickupBulb()
        check_pos\XYZ:=pickupXYZ;
        OpenGripper;
        MoveJ [[0, 0, 304.8], [0, 0, 1, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=PickupWobj;
        MoveL [[0, 0, 0], [0, 0, 1, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=PickupWobj;
        CloseGripper;
        MoveL [[0, 0, 304.8], [0, 0, 1, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=PickupWobj;
        check_pos\XYZ:=pickupXYZ;
    ENDPROC
    
    PROC ScrewInBulb()

        VAR num rightytighty := 180;
        VAR num leftyloosey := -180;
        
        check_pos\XYZ:=dropoffXYZ;
        WaitRob\InPos;
        CloseGripper;
        ScrewPos0a.robax.rax_6 := leftyloosey;
        ScrewPos1.robax.rax_6 := leftyloosey;
        MoveAbsJ ScrewPos0a, v500, z5, BulbGripper\WObj:=DropoffWobj;
        MoveAbsJ ScrewPos1, v500, z0, BulbGripper\WObj:=DropoffWobj;
        
        
        WaitRob\InPos;
        CloseGripper;
        ScrewPos2.robax.rax_6 := rightytighty;
        MoveAbsJ ScrewPos2, v500, z0, BulbGripper\WObj:=DropoffWobj;
        
        WaitRob\InPos;
        OpenGripper;
        ScrewPos2.robax.rax_6 := leftyloosey;
        MoveAbsJ ScrewPos2, v500, z0, BulbGripper\WObj:=DropoffWobj;
        
        WaitRob\InPos;
        CloseGripper;
        ScrewPos3.robax.rax_6 := rightytighty;
        MoveAbsJ ScrewPos3, v500, z0, BulbGripper\WObj:=DropoffWobj;
        
        WaitRob\InPos;
        OpenGripper;
        ScrewPos3.robax.rax_6 := leftyloosey;
        MoveAbsJ ScrewPos3, v500, z0, BulbGripper\WObj:=DropoffWobj;
        
        WaitRob\InPos;
        CloseGripper;
        ScrewPos4.robax.rax_6 := rightytighty;
        MoveAbsJ ScrewPos4, v500, z0, BulbGripper\WObj:=DropoffWobj;
        
        WaitRob\InPos;
        OpenGripper;
        ScrewPos4.robax.rax_6 := rightytighty;
        MoveAbsJ ScrewPos4, v500, z0, BulbGripper\WObj:=DropoffWobj;
        
        
        ScrewPos0a.robax.rax_6 := rightytighty;
        ScrewPos1.robax.rax_6 := rightytighty;
        ScrewPos2.robax.rax_6 := rightytighty;
        ScrewPos3.robax.rax_6 := rightytighty;
        ScrewPos4.robax.rax_6 := rightytighty;
        MoveAbsJ ScrewPos4, v500, z1, BulbGripper\WObj:=DropoffWobj;
        MoveAbsJ ScrewPos3, v500, z1, BulbGripper\WObj:=DropoffWobj;
        MoveAbsJ ScrewPos2, v500, z1, BulbGripper\WObj:=DropoffWobj;
        MoveAbsJ ScrewPos1, v500, z1, BulbGripper\WObj:=DropoffWobj;
        MoveAbsJ ScrewPos0a, v500, z1, BulbGripper\WObj:=DropoffWobj;
        check_pos\XYZ:=dropoffXYZ;
        
    ENDPROC
    
    PROC UnscrewBulb()
        
        VAR num rightytighty := 300;
        VAR num leftyloosey := -300;
        
        check_pos\XYZ:=dropoffXYZ;
        WaitRob\InPos;
        OpenGripper;
        ScrewPos0a.robax.rax_6 := rightytighty;
        ScrewPos1.robax.rax_6 := rightytighty;
        ScrewPos2.robax.rax_6 := rightytighty;
        ScrewPos3.robax.rax_6 := rightytighty;
        ScrewPos4.robax.rax_6 := rightytighty;
        MoveAbsJ ScrewPos0a, v500, z5, BulbGripper\WObj:=DropoffWobj;
        MoveAbsJ ScrewPos1, v500, z0, BulbGripper\WObj:=DropoffWobj;
        MoveAbsJ ScrewPos2, v500, z0, BulbGripper\WObj:=DropoffWobj;
        MoveAbsJ ScrewPos3, v500, z0, BulbGripper\WObj:=DropoffWobj;
        MoveAbsJ ScrewPos4, v500, z0, BulbGripper\WObj:=DropoffWobj;
        
        
        WaitRob\InPos;
        CloseGripper;
        ScrewPos3.robax.rax_6 := leftyloosey;
        MoveAbsJ ScrewPos3, v500, z0, BulbGripper\WObj:=DropoffWobj;
        WaitRob\InPos;
        OpenGripper;
        ScrewPos3.robax.rax_6 := rightytighty;
        MoveAbsJ ScrewPos3, v500, z0, BulbGripper\WObj:=DropoffWobj;
        
        WaitRob\InPos;
        CloseGripper;
        ScrewPos2.robax.rax_6 := leftyloosey;
        MoveAbsJ ScrewPos2, v500, z0, BulbGripper\WObj:=DropoffWobj;
        WaitRob\InPos;
        CloseGripper;
        ScrewPos1.robax.rax_6 := leftyloosey;
        MoveAbsJ ScrewPos2, v500, z0, BulbGripper\WObj:=DropoffWobj;
        WaitRob\InPos;
        
        !WaitRob\InPos;
        !CloseGripper;
        !ScrewPos1.robax.rax_6 := finalRotation;
        !MoveAbsJ ScrewPos1, v500, z0, BulbGripper\WObj:=DropoffWobj;
        !WaitRob\InPos;
        !CloseGripper;
        !ScrewPos1.robax.rax_6 := finalRotation;
        !MoveAbsJ ScrewPos1, v500, z0, BulbGripper\WObj:=DropoffWobj;
        
        
        ScrewPos0a.robax.rax_6 := leftyloosey;
        MoveAbsJ ScrewPos0a, v500, z1, BulbGripper\WObj:=DropoffWobj;
        check_pos\XYZ:=dropoffXYZ;
    ENDPROC
    
    PROC PlacebulbBack()
        check_pos\XYZ:=pickupXYZ;
        CloseGripper;
        MoveJ [[0, 0, 304.8], [0, 0, 1, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=PickupWobj;
        MoveL [[0, 0, 0], [0, 0, 1, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=PickupWobj;
        OpenGripper;
        MoveL [[0, 0, 304.8], [0, 0, 1, 0], [0,0,0,0], [9E9, 9E9, 9E9, 9E9, 9E9, 9E9]], v500, z20, BulbGripper\WObj:=PickupWobj;
        check_pos\XYZ:=pickupXYZ;
    ENDPROC
    
    
    PROC randomize_screwin()
        DropoffWobj.oframe.trans.X := rand(\min:=-1000,\max:=1000);
        DropoffWobj.oframe.trans.Y := rand(\min:=-1200,\max:=1200);
    ENDPROC
    
    PROC randomize_pickup()
        PickupWobj.oframe.trans.X := rand(\min:=-400,\max:=800);
        PickupWobj.oframe.trans.Y := rand(\min:=-1670,\max:=-1670);
    ENDPROC
    
    
ENDMODULE