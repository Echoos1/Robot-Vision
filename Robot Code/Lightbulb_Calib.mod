MODULE Lightbulb_Calib

    !*****************************************************
    !Module Name:   Lightbulb_Calib
    !Version:       1.0
    !Description:   A script to calibrate the position of the lightbulb demonstration
    !Date Created:  2 June 2023
    !Date Updated   -
    !Author:        Matthew DiMaggio
    !*****************************************************
    
    
    
    VAR num Incrament:=1;

    
    PROC LightCalib()
        
        check := StrToVal(ValToStr(PickupWobj.oframe.trans.X),pickupX);
        check := StrToVal(ValToStr(PickupWobj.oframe.trans.Y),pickupY);
        check := StrToVal(ValToStr(DropoffWobj.oframe.trans.X),dropoffX);
        check := StrToVal(ValToStr(DropoffWobj.oframe.trans.Y),dropoffY);
        dropoffXYZ := [dropoffX,dropoffY,0];
        pickupXYZ := [pickupX,pickupY,0];
        
        PickupCalib;
        DropoffCalib;
        check_pos\XYZ:=pickupXYZ;
        MoveJ [[0,0,304.8],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
        MoveL [[0,0,0],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
        OpenGripper;
        MoveL [[0,0,304.8],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
        check_pos\XYZ:=pickupXYZ;
        MoveAbsJ ZeroPoint,v500,z0,BulbGripper\WObj:=wobj0;
        Stop;
    ENDPROC

    PROC PickupCalib()
        check_pos\XYZ:=pickupXYZ;
        OpenGripper;
        MoveJ [[0,0,304.8],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
        MoveL [[0,0,0],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
        PickupCalibLoop;
        CloseGripper;
        MoveL [[0,0,304.8],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
        check_pos\XYZ:=pickupXYZ;
    ENDPROC


    PROC PickupCalibLoop()

        Reset_Regs;
        TPReadFK reg1,"Adjust Pickup Location","Adjust X","Adjust Y","Adjust Z","Incr.","Done";

        IF reg1=1 THEN
            AdjustPickupX;
        ELSEIF reg1=2 THEN
            AdjustPickupY;
        ELSEIF reg1=3 THEN
            AdjustPickupZ;
        ELSEIF reg1=4 THEN
            AdjustIncrament;
        ENDIF
        Reset_Regs;
    ENDPROC


    PROC AdjustIncrament()
        Reset_Regs;
        TPReadFK reg3,"Adjust Calibration Incrament","1","2","5","10","50";
        IF reg3=1 THEN
            Incrament:=1;
        ELSEIF reg3=2 THEN
            Incrament:=2;
        ELSEIF reg3=3 THEN
            Incrament:=5;
        ELSEIF reg3=4 THEN
            Incrament:=10;
        ELSEIF reg3=5 THEN
            Incrament:=50;
        ENDIF
    ENDPROC


    PROC AdjustPickupX()
        Reset_Regs;
        TPReadFK reg2,"Adjust Pickup X","+X","-X",stEmpty,"Incr.","Done";
        IF reg2=1 THEN
            PickupWobj.oframe.trans.X:=PickupWobj.oframe.trans.X+Incrament;
            MoveL [[0,0,0],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
            AdjustPickupX;
        ELSEIF reg2=2 THEN
            PickupWobj.oframe.trans.X:=PickupWobj.oframe.trans.X-Incrament;
            MoveL [[0,0,0],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
            AdjustPickupX;
        ELSEIF reg2=4 THEN
            AdjustIncrament;
            AdjustPickupX;
        ELSEIF reg2=5 THEN
            PickupCalibLoop;
        ENDIF

    ENDPROC


    PROC AdjustPickupY()
        Reset_Regs;
        TPReadFK reg2,"Adjust Pickup Y","+Y","-Y",stEmpty,"Incr.","Done";
        IF reg2=1 THEN
            PickupWobj.oframe.trans.Y:=PickupWobj.oframe.trans.Y+Incrament;
            MoveL [[0,0,0],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
            AdjustPickupY;
        ELSEIF reg2=2 THEN
            PickupWobj.oframe.trans.Y:=PickupWobj.oframe.trans.Y-Incrament;
            MoveL [[0,0,0],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
            AdjustPickupY;
        ELSEIF reg2=4 THEN
            AdjustIncrament;
            AdjustPickupY;
        ELSEIF reg2=5 THEN
            PickupCalibLoop;
        ENDIF
    ENDPROC


    PROC AdjustPickupZ()
        Reset_Regs;
        TPReadFK reg2,"Adjust Pickup Z","+Z","-Z",stEmpty,"Incr.","Done";
        IF reg2=1 THEN
            PickupWobj.oframe.trans.Z:=PickupWobj.oframe.trans.Z+Incrament;
            MoveL [[0,0,0],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
            AdjustPickupZ;
        ELSEIF reg2=2 THEN
            PickupWobj.oframe.trans.Z:=PickupWobj.oframe.trans.Z-Incrament;
            MoveL [[0,0,0],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=PickupWobj;
            AdjustPickupZ;
        ELSEIF reg2=4 THEN
            AdjustIncrament;
            AdjustPickupZ;
        ELSEIF reg2=5 THEN
            PickupCalibLoop;
        ENDIF
    ENDPROC

    PROC DropoffCalib()
        check_pos\XYZ:=dropoffXYZ;
        CloseGripper;

        MoveJ [[0,0,-300],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=DropoffWobj;
        MoveL [[0,0,-24.18],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=DropoffWobj;
        DropoffCalibLoop;
        MoveL [[0,0,-300],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=DropoffWobj;
        check_pos\XYZ:=dropoffXYZ;
    ENDPROC


    PROC DropoffCalibLoop()

        Reset_Regs;
        TPReadFK reg1,"Adjust Dropoff Location","Adjust X","Adjust Y","Adjust Z","Incr.","Done";

        IF reg1=1 THEN
            AdjustDropoffX;
        ELSEIF reg1=2 THEN
            AdjustDropoffY;
        ELSEIF reg1=3 THEN
            AdjustDropoffZ;
        ELSEIF reg1=4 THEN
            AdjustIncrament;
        ENDIF
        Reset_Regs;
    ENDPROC


    PROC AdjustDropoffX()
        Reset_Regs;
        TPReadFK reg2,"Adjust Dropoff X","+X","-X",stEmpty,"Incr.","Done";
        IF reg2=1 THEN
            DropoffWobj.oframe.trans.X:=DropoffWobj.oframe.trans.X+Incrament;
            MoveL [[0,0,-24.18],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=DropoffWobj;
            AdjustDropoffX;
        ELSEIF reg2=2 THEN
            DropoffWobj.oframe.trans.X:=DropoffWobj.oframe.trans.X-Incrament;
            MoveL [[0,0,-24.18],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=DropoffWobj;
            AdjustDropoffX;
        ELSEIF reg2=4 THEN
            AdjustIncrament;
            AdjustDropoffX;
        ELSEIF reg2=5 THEN
            DropoffCalibLoop;
        ENDIF

    ENDPROC


    PROC AdjustDropoffY()
        Reset_Regs;
        TPReadFK reg2,"Adjust Dropoff Y","+Y","-Y",stEmpty,"Incr.","Done";
        IF reg2=1 THEN
            DropoffWobj.oframe.trans.Y:=DropoffWobj.oframe.trans.Y+Incrament;
            MoveL [[0,0,-24.18],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=DropoffWobj;
            AdjustDropoffY;
        ELSEIF reg2=2 THEN
            DropoffWobj.oframe.trans.Y:=DropoffWobj.oframe.trans.Y-Incrament;
            MoveL [[0,0,-24.18],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=DropoffWobj;
            AdjustDropoffY;
        ELSEIF reg2=4 THEN
            AdjustIncrament;
            AdjustDropoffY;
        ELSEIF reg2=5 THEN
            DropoffCalibLoop;
        ENDIF
    ENDPROC


    PROC AdjustDropoffZ()
        Reset_Regs;
        TPReadFK reg2,"Adjust Dropoff Z","+Z","-Z",stEmpty,"Incr.","Done";
        IF reg2=1 THEN
            DropoffWobj.oframe.trans.Z:=DropoffWobj.oframe.trans.Z+Incrament;
            MoveL [[0,0,-24.18],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=DropoffWobj;
            AdjustDropoffZ;
        ELSEIF reg2=2 THEN
            DropoffWobj.oframe.trans.Z:=DropoffWobj.oframe.trans.Z-Incrament;
            MoveL [[0,0,-24.18],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]],v500,z20,BulbGripper\WObj:=DropoffWobj;
            AdjustDropoffZ;
        ELSEIF reg2=4 THEN
            AdjustIncrament;
            AdjustDropoffZ;
        ELSEIF reg2=5 THEN
            DropoffCalibLoop;
        ENDIF
    ENDPROC

ENDMODULE