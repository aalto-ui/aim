db = new Mongo().getDB("aim");

db.createCollection("inputs", { capped: false });
db.createCollection("results", { capped: false });
