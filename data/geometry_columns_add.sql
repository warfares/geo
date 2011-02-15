/* adjust geometry_columns table for pre-calculated values */ 

/* layer-bbox */

ALTER TABLE geometry_columns
   ADD COLUMN "left" double precision;

ALTER TABLE geometry_columns
   ADD COLUMN "bottom" double precision;

ALTER TABLE geometry_columns
   ADD COLUMN "right" double precision;

ALTER TABLE geometry_columns
   ADD COLUMN "top" double precision;
