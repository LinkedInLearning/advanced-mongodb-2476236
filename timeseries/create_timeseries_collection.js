db.createCollection("stocks_timeseries", {
  timeseries: {
    timeField: "ts",
    metaField: "ticker",
    granularity: "hours",
  },
});
