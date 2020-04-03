CREATE OR REPLACE VIEW
  `moz-fx-data-shared-prod.telemetry.firefox_desktop_exact_mau28_by_dimensions_v1`
AS
SELECT
  raw.*,
  COALESCE(cc.name, raw.country) AS country_name
FROM
  `moz-fx-data-derived-datasets.telemetry_derived.firefox_desktop_exact_mau28_by_dimensions_v1` AS raw
LEFT JOIN
  `moz-fx-data-shared-prod.static.country_codes_v1` cc
ON
  (raw.country = cc.code)