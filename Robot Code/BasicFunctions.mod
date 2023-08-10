MODULE BasicFunctions
    
    PROC Reset_Regs()
        reg1 := 0;
        reg2 := 0;
        reg3 := 0;
        reg4 := 0;
        reg5 := 0;
    ENDPROC
    
    FUNC num rand(\num min,\num max)
        RETURN ((((((2/pi)*ASin(Abs(Sin(pi*(GetTime(\Sec)*min*max))))))*(pi/180))*(max-min)))+min;
    ENDFUNC
    
    FUNC orient MultiplyQuaternions(orient Q0,orient Q1)
        RETURN [Q0.q1*Q1.q1-Q0.q2*Q1.q2-Q0.q3*Q1.q3-Q0.q4*Q1.q4, 
            Q0.q1*Q1.q2+Q0.q2*Q1.q1+Q0.q3*Q1.q4-Q0.q4*Q1.q3, 
                Q0.q1*Q1.q3-Q0.q2*Q1.q4+Q0.q3*Q1.q1+Q0.q4*Q1.q2, 
                    Q0.q1*Q1.q4+Q0.q2*Q1.q3-Q0.q3*Q1.q2+Q0.q4*Q1.q1];
    ENDFUNC
    
    
ENDMODULE