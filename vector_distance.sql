drop function vdistance(double precision[], double precision[]);
Create function vdistance(double precision[], double precision[])
RETURNS double precision
AS $$
DECLARE
	ret_sum double precision;
	sum1 double precision;
BEGIN
	ret_sum := 0;
	for i in 1..array_length($1,1) LOOP
		sum1:= $1[i]-$2[i];
		ret_sum=ret_sum+pow(sum1,2);
	END LOOP;
	return sqrt(ret_sum);
END
$$ language 'plpgsql';