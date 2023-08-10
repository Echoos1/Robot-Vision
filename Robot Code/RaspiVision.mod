MODULE RaspiVision
    !*****************************************************
    !Module Name:   RaspiVision
    !Version:       1.0
    !Description:   Takes the input from a Raspberry Pi Camera and locates a marker
    !Date Created:  17 July 2023
    !Date Updated:  9 August 2023
    !Author:        Matthew DiMaggio
    !*****************************************************

    RECORD Binary
        num BiS;
        num Bi11;
        num Bi10;
        num Bi9;
        num Bi8;
        num Bi7;
        num Bi6;
        num Bi5;
        num Bi4;
        num Bi3;
        num Bi2;
        num Bi1;
    ENDRECORD

    VAR Binary bin;
    VAR dnum binNum;
    
    VAR num pulseLength := 0.125;
    
    CONST jointtarget scanNeutral:=[[0,-60,30,0,70,0],[9E9,9E9,9E9,9E9,9E9,9E9]];

    VAR jointtarget testPose:=[[-63.7,-23.6,25.9,-0.1,42.6,-1.4],[9E9,9E9,9E9,9E9,9E9,9E9]];
    VAR jointtarget testPose2:=[[-34.2,-6.6,-1.4,-36.8,76.6,-1.4],[9E9,9E9,9E9,9E9,9E9,9E9]];
    VAR jointtarget testPose3:=[[12.2,1.9,-19.4,-62.9,107.1,-72.0],[9E9,9E9,9E9,9E9,9E9,9E9]];
    VAR jointtarget testPose4:=[[-63.7,-23.6,25.9,-0.1,42.6,-1.4],[9E9,9E9,9E9,9E9,9E9,9E9]];
    VAR robtarget calibPose:=[[924.3,-1488.4,1180.5],[0,0,1,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];

    VAR robtarget pickupRefine1:=[[95,115,1000],[0,1,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
    VAR robtarget pickupAlign:=[[95,115,100],[0,1,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];

    !********************************
    ! Inputs from the RaspiCam
    PERS num raspiPickX:=-63.703;
    PERS num raspiPickY:=216.513;
    PERS num raspiPickZ:=897.364;
    PERS num raspiPickQW:=-0.019952;
    PERS num raspiPickQX:=0.999754;
    PERS num raspiPickQY:=-0.006024;
    PERS num raspiPickQZ:=-0.004888;
    !********************************
    !********************************
    ! Inputs from the RaspiCam
    PERS num raspiDropX:=0;
    PERS num raspiDropY:=0;
    PERS num raspiDropZ:=0;
    PERS num raspiDropQW:=0;
    PERS num raspiDropQX:=0;
    PERS num raspiDropQY:=0;
    PERS num raspiDropQZ:=0;
    !********************************
    CONST num XAdjust:=-0.003141;
    CONST num YAdjust:=0.016537;
    CONST num ZAdjust:=1.28032;

    PERS robtarget curCamPose;
    VAR robtarget newTarget;

    PROC newPickWObj()
        curCamPose:=CRobt(\Tool:=RaspiCamTool,\WObj:=wobj0);
        newTarget:=RelTool(curCamPose,raspiPickX*XAdjust,raspiPickY*YAdjust,raspiPickZ*ZAdjust,\Rx:=0,\Ry:=0,\Rz:=0);
        PickupArUCo.oframe.trans:=newTarget.trans;
        PickupArUCo.oframe.rot:=NOrient(MultiplyQuaternions(curCamPose.rot,NOrient([raspiPickQW,raspiPickQX,raspiPickQY,raspiPickQZ])));
    ENDPROC


    PROC newDropWObj()
        curCamPose:=CRobt(\Tool:=RaspiCamTool,\WObj:=wobj0);
        newTarget:=RelTool(curCamPose,raspiPickX*XAdjust,raspiPickY*YAdjust,raspiPickZ*ZAdjust,\Rx:=0,\Ry:=0,\Rz:=0);
        PickupArUCo.oframe.trans:=newTarget.trans;
        PickupArUCo.oframe.rot:=MultiplyQuaternions(curCamPose.rot,[raspiPickQW,raspiPickQX,raspiPickQY,raspiPickQZ]);
    ENDPROC


    PROC VisionInit()
        ! Do stuff before taking picture
        TPWrite("Moving to initial pose");
        MoveAbsJ scanNeutral,v500,z20,RaspiCamTool\WObj:=wobj0;
        TPWrite("Waiting for user to continue... [Press play to continue]");
        Stop;
        VisionMain;
    ENDPROC



    PROC VisionMain()
        ! Send Take Picture Signal
        TPWrite("Sending Take Picture Command...");
        WaitDI DI10_CamStep,1;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;
        
        TPWrite("Waiting for Photo...");
        WaitDI DI10_CamStep,1;
        TPWrite("Reading Pose");
        readCamPose;

        TPWrite("Calculating new pose...");
        newPickWObj;
        !newDropWObj;
        
        TPWrite("Moving to aligned pose...");
        MoveJ pickupAlign,v200,z20,BulbGripper\WObj:=PickupArUCo;
        
        TPWrite("Wait 3");
        WaitTime(3);
        VisionInit;
    ENDPROC


    PROC readBin()
        WaitTime(0.125);
        binNum := 0;
        IF DI10_Bi1=1 THEN
            binNum := binNum + 1;
        ENDIF
        IF DI10_Bi2=1 THEN
            binNum := binNum + 2;
        ENDIF
        IF DI10_Bi3=1 THEN
            binNum := binNum + 4;
        ENDIF
        IF DI10_Bi4=1 THEN
            binNum := binNum + 8;
        ENDIF
        IF DI10_Bi5=1 THEN
            binNum := binNum + 16;
        ENDIF
        IF DI10_Bi6=1 THEN
            binNum := binNum + 32;
        ENDIF
        IF DI10_Bi7=1 THEN
            binNum := binNum + 64;
        ENDIF
        IF DI10_Bi8=1 THEN
            binNum := binNum + 128;
        ENDIF
        IF DI10_Bi9=1 THEN
            binNum := binNum + 256;
        ENDIF
        IF DI10_Bi10=1 THEN
            binNum := binNum + 512;
        ENDIF
        IF DI10_Bi11=1 THEN
            binNum := binNum + 1024;
        ENDIF
        IF DI10_BiS=1 THEN
            binNum := binNum * (-1);
        ENDIF
        TPWrite(ValToStr(binNum));
    ENDPROC
    
    
    PROC readCamPose()
        VAR dnum pX;
        VAR dnum pY;
        VAR dnum pZ;
        VAR dnum pQW;
        VAR dnum pQX;
        VAR dnum pQY;
        VAR dnum pQZ;
        VAR dnum dX;
        VAR dnum dY;
        VAR dnum dZ;
        VAR dnum dQW;
        VAR dnum dQX;
        VAR dnum dQY;
        VAR dnum dQZ;

        !!!!!! PICKUP BOARD
        !!! Pickup X
        ! Read Pickup X Whole
        TPWrite("Reading Pickup X Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        pX:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Pickup X Decimal
        TPWrite("Reading Pickup X Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        pX:=pX+(binNum/1000);
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Pickup Y
        ! Read Pickup Y Whole
        TPWrite("Reading Pickup Y Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        pY:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Pickup Y Decimal
        TPWrite("Reading Pickup Y Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        pY:=pY+(binNum/1000);
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Pickup Z
        ! Read Pickup Z Whole
        TPWrite("Reading Pickup Z Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        pZ:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Pickup Z Decimal
        TPWrite("Reading Pickup Z Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        pZ:=pZ+(binNum/1000);
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Pickup QW
        ! Read Pickup QW Whole
        TPWrite("Reading Pickup QW Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        pQW:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Pickup QW Decimal
        TPWrite("Reading Pickup QW Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        pQW:=(pQW+(binNum/1000))/1000;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Pickup QX
        ! Read Pickup QX Whole
        TPWrite("Reading Pickup QX Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        pQX:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Pickup QX Decimal
        TPWrite("Reading Pickup QX Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        pQX:=(pQX+(binNum/1000))/1000;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Pickup QY
        ! Read Pickup QY Whole
        TPWrite("Reading Pickup QY Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        pQY:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Pickup QY Decimal
        TPWrite("Reading Pickup QY Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        pQY:=(pQY+(binNum/1000))/1000;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Pickup QZ
        ! Read Pickup QZ Whole
        TPWrite("Reading Pickup QZ Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        pQZ:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Pickup QZ Decimal
        TPWrite("Reading Pickup QZ Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        pQZ:=(pQZ+(binNum/1000))/1000;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!!!!! DROPOFF BOARD
        !!! Dropoff X
        ! Read Dropoff X Whole
        TPWrite("Reading Dropoff X Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        dX:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Dropoff X Decimal
        TPWrite("Reading Dropoff X Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        dX:=dX+(binNum/1000);
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Dropoff Y
        ! Read Dropoff Y Whole
        TPWrite("Reading Dropoff Y Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        dY:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;
        
        ! Read Dropoff Y Decimal
        TPWrite("Reading Dropoff Y Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        dY:=dY+(binNum/1000);
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Dropoff Z
        ! Read Dropoff Z Whole
        TPWrite("Reading Dropoff Z Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        dZ:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Dropoff Z Decimal
        TPWrite("Reading Dropoff Z Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        dZ:=dZ+(binNum/1000);
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Dropoff QW
        ! Read Dropoff QW Whole
        TPWrite("Reading Dropoff QW Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        dQW:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Dropoff QW Decimal
        TPWrite("Reading Dropoff QW Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        dQW:=(dQW+(binNum/1000))/1000;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Dropoff QX
        ! Read Dropoff QX Whole
        TPWrite("Reading Dropoff QX Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        dQX:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Dropoff QX Decimal
        TPWrite("Reading Dropoff QX Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        dQX:=(dQX+(binNum/1000))/1000;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Dropoff QY
        ! Read Dropoff QY Whole
        TPWrite("Reading Dropoff QY Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        dQY:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Dropoff QY Decimal
        TPWrite("Reading Dropoff QY Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        dQY:=(dQY+(binNum/1000))/1000;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        !!! Dropoff QZ
        ! Read Dropoff QZ Whole
        TPWrite("Reading Dropoff QZ Whole...");
        WaitDI DI10_CamStep,1;
        readBin;
        dQZ:=binNum;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;

        ! Read Dropoff QZ Decimal
        TPWrite("Reading Dropoff QZ Decimal...");
        WaitDI DI10_CamStep,1;
        readBin;
        dQZ:=(dQZ+(binNum/1000))/1000;
        PulseDO\PLength:=pulseLength,DO10_robStep;
        WaitDI DI10_CamStep,0;
        
        TPWrite("Reassigning RaspiVision Vals");
        TPWrite("Pickup ArUCo: ");
        TPWrite(ValToStr(pX));
        raspiPickX:=DnumToNum(pX);
        TPWrite(ValToStr(pY));
        raspiPickY:=DnumToNum(pY);
        TPWrite(ValToStr(pZ));
        raspiPickZ:=DnumToNum(pZ);
        TPWrite(ValToStr(pQW));
        raspiPickQW:=DnumToNum(pQW);
        TPWrite(ValToStr(pQX));
        raspiPickQX:=DnumToNum(pQX);
        TPWrite(ValToStr(pQY));
        raspiPickQY:=DnumToNum(pQY);
        TPWrite(ValToStr(pQZ));
        raspiPickQZ:=DnumToNum(pQZ);

        raspiDropX:=DnumToNum(dX);
        raspiDropY:=DnumToNum(dY);
        raspiDropZ:=DnumToNum(dZ);
        raspiDropQW:=DnumToNum(dQW);
        raspiDropQX:=DnumToNum(dQX);
        raspiDropQY:=DnumToNum(dQY);
        raspiDropQZ:=DnumToNum(dQZ);
    ENDPROC


ENDMODULE