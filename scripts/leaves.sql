-- Table: leaves

-- DROP TABLE leaves;
CREATE DATABASE leaves
  WITH OWNER = postgres
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'C'
       LC_CTYPE = 'C'
       CONNECTION LIMIT = -1;


CREATE TABLE leaves
(
  "name" character varying(25) NOT NULL,
  "common_name" character varying(25),
  wiki text,
  descriptors double precision[],
  photo text,
  CONSTRAINT leaves_pkey PRIMARY KEY (name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE leaves OWNER TO postgres;

-- Index: leaves_descriptors_idx

-- DROP INDEX leaves_descriptors_idx;

CREATE INDEX leaves_descriptors_idx
  ON leaves
  USING btree
  (descriptors);

CREATE OR REPLACE FUNCTION vdistance(double precision[], double precision[])
  RETURNS double precision AS
$BODY$
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
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION vdistance(double precision[], double precision[]) OWNER TO postgres;
