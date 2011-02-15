-- Function: build_bbox()
-- DROP FUNCTION build_bbox();

CREATE OR REPLACE FUNCTION build_bbox()
  RETURNS character varying AS
$BODY$
DECLARE                                                	
	table_record record; 
	bbox_record record;		                                                                                                                                                   
BEGIN                				
	FOR table_record IN 
		select f_table_schema, f_table_name, srid from geometry_columns where "left" is null 
	LOOP		
		RAISE NOTICE 'working with; %', table_record.f_table_name;
	
		-- layer projection to  WSM  (static bbox)!! 
		-- TODO: try to execute without a cicle, is just one cicle. !!
		FOR bbox_record IN EXECUTE
			'SELECT  ST_XMin(transform(ST_SetSRID(r.box,' || table_record.srid || '), 96)) AS b_left, 
			ST_YMin(transform(ST_SetSRID(r.box,' || table_record.srid || '), 96)) AS b_bottom, 
			ST_XMax(transform(ST_SetSRID(r.box,' || table_record.srid || '), 96)) AS b_right, 
			ST_YMax(transform(ST_SetSRID(r.box,' || table_record.srid || '), 96)) AS b_top 
			FROM
			(SELECT EXTENT(the_geom) AS box FROM ' || table_record.f_table_schema || '.'|| table_record.f_table_name || ') AS r'
		LOOP 		
			UPDATE geometry_columns
			SET "left"  = bbox_record.b_left,
			"bottom" = bbox_record.b_bottom,
			"right" = bbox_record.b_right, 
			"top" = bbox_record.b_top
			WHERE f_table_name = table_record.f_table_name
			AND f_table_schema = table_record.f_table_schema;	

			RAISE NOTICE 'update bbox OK !!';	
		END LOOP;		
	END LOOP; 			
		RAISE NOTICE 'All OK';							
RETURN '';
	
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION build_bbox() OWNER TO postgres;