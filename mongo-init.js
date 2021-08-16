db = new Mongo().getDB("aim");

db.createCollection("errors", { capped: false });
db.createCollection("inputs", { capped: false });
db.createCollection("results", { capped: false });
