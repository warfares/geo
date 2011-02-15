update spatial_ref_sys
set proj4text = '+proj=utm +zone=19 +south +ellps=intl +towgs84=-307.7,265.3,-363.5, 0, 0, 0, 0 +units=m +no_defs'
where srid = 24879