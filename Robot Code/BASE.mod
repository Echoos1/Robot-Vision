MODULE BASE (SYSMODULE, NOSTEPIN, VIEWONLY)
    
    ! This RAPID code was generated with RobotComponents v1.5.1 (GPL v3)
    ! Visit www.github.com/RobotComponents for more information
    
    ! System module with basic predefined system data
    ! ***********************************************
    
    ! System data tool0, wobj0 and load0
    ! Do not translate or delete tool0, wobj0, load0
    PERS tooldata tool0 := [TRUE, [[0, 0, 0], [1, 0, 0, 0]], [0.001, [0, 0, 0.001], [1, 0, 0, 0], 0, 0, 0]];
    PERS wobjdata wobj0 := [FALSE, TRUE, "" , [[0, 0, 0], [1, 0, 0, 0]], [[0, 0, 0], [1, 0, 0, 0]]];
    PERS loaddata load0 := [0.001, [0, 0, 0.001], [1, 0, 0, 0], 0, 0, 0];
    
    ! User defined tooldata
    PERS tooldata BulbGripper := [TRUE, [[0, 0, 167.069], [1, 0, 0, 0]], [0.001, [0, 0, 0.001], [1, 0, 0, 0], 0, 0, 0]];
    PERS tooldata RaspiCamTool := [TRUE, [[0, 99.5, 135.2], [-0.707107, 0, 0, 0.707107]], [0.001, [0, 0, 0.001], [1, 0, 0, 0], 0, 0, 0]];

    ! User defined wobjdata
    PERS wobjdata PickupWobj := [FALSE, TRUE, "", [[0, 0, 0], [1, 0, 0, 0]], [[167, -1455, 640], [1, 0, 0, 0]]];
    PERS wobjdata DropoffWobj := [FALSE, TRUE, "", [[0, 0, 0], [1, 0, 0, 0]], [[-308, -1565, 650], [0, 1, 0, 0]]];
    PERS wobjdata PickupArUCo := [FALSE, TRUE, "", [[0, 0, 0], [1, 0, 0, 0]], [[1224.26, 99.2999, 661.621], [0.637147, 0.306621, -0.316487, -0.632347]]];
    PERS wobjdata DropoffArUCo := [FALSE, TRUE, "", [[0, 0, 0], [1, 0, 0, 0]], [[819, -1433, 650], [0, 1, 0, 0]]];
    
ENDMODULE