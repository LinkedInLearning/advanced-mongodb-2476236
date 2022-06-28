db.stocks.aggregate([
  {
    $project: {
      date: {
        $dateToParts: { date: "$date" },
      },
      price: 1,
      ticker: 1,
    },
  },
  {
    $group: {
      _id: {
        ticker: "$ticker",
        date: {
          year: "$date.year",
          month: "$date.month",
          day: "$date.day",
        },
      },
      avgPrice: { $avg: "$price" },
    },
  },
  { $merge: "stocksDailyAvgView" },
]);
