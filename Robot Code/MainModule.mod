MODULE MainModule

    !*****************************************************
    !Module Name:   MainModule
    !Version:       1.3
    !Description:   Contains the main procedure, which gives the robot the order in which it must perform its other tasks
    !Date Created:  25 May 2023
    !Date Updated:  8 August 2023
    !Author:        Matthew DiMaggio
    !*****************************************************




    VAR jointtarget ZeroPoint:=[[0,-45,45,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
    VAR jointtarget ZeroPointNeg:=[[-90,-45,45,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
    VAR jointtarget ZeroPointPos:=[[90,-45,45,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];

    PROC main()
        TPErase;
        TPWrite("[START PROGRAM]");

        ConfJ\off;
        ConfL\off;

        ! Setup Reset Parameters and Prepare Syncornization
        SetDO DO10_robReady,0;
        TPWrite("Waiting for Camera Ready...");
        WHILE binNum<>(-1755) DO
            readBin;
        ENDWHILE
        TPWrite("Camera Ready!");
        SetDO DO10_robReady,1;

        TPWrite("Establishing Handshake...");
        WaitDI DI10_CamStep,1;
        PulseDO\PLength:=0.25,DO10_robStep;
        TPWrite("Handshake Established!");

        VisionInit;
    ENDPROC

    ! Checks the position of the work object
    ! to set robot to closest and most relaible base point with MoveAbsJ
    PROC check_pos(\VAR pos XYZ)

        VAR pos zp0:=[800.672636,0,0];
        VAR pos zpn:=[0,-800.672636,0];
        VAR pos zpp:=[0,800.672636,0];

        !CONST num zero := Distance(XYZ,[800.672636,0,1306.396103]);
        !CONST num zeroneg := Distance(XYZ,[0,-800.672636,1306.396103]);
        !CONST num zeropos := Distance(XYZ,[0,800.672636,1306.396103]);

        IF Distance(XYZ,zp0)<Distance(XYZ,zpn) AND Distance(XYZ,zp0)<Distance(XYZ,zpp) THEN
            MoveAbsJ ZeroPoint,v500,z50,BulbGripper\WObj:=wobj0;
        ELSEIF Distance(XYZ,zpn)<Distance(XYZ,zp0) AND Distance(XYZ,zpn)<Distance(XYZ,zpp) THEN
            MoveAbsJ ZeroPointNeg,v500,z50,BulbGripper\WObj:=wobj0;
        ELSEIF Distance(XYZ,zpp)<Distance(XYZ,zp0) AND Distance(XYZ,zpp)<Distance(XYZ,zpn) THEN
            MoveAbsJ ZeroPointPos,v500,z50,BulbGripper\WObj:=wobj0;
        ELSE
            MoveAbsJ ZeroPoint,v500,z0,BulbGripper\WObj:=wobj0;
        ENDIF

    ENDPROC

ENDMODULE
