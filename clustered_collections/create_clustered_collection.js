db.createCollection("stocksMDBClustered", {
  clusteredIndex: {
    key: { _id: 1 },
    unique: true,
    name: "stocks clustered index",
  },
});
