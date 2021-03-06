CREATE TABLE "customer" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL,
	"mob1"	INTEGER NOT NULL,
	"mob2"	INTEGER NOT NULL,
	"address"	TEXT NOT NULL,
	"city"	TEXT NOT NULL,
	"aadhar_card"	TEXT NOT NULL,
	"photo"	TEXT NOT NULL,
	"created_date"	TEXT NOT NULL,
	"email"	TEXT
);
CREATE TABLE "item" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL,
	"desc"	TEXT NOT NULL,
	"weight"	NUMERIC NOT NULL,
	"photo"	TEXT,
	"created_date"	TEXT NOT NULL,
	"stock"	INTEGER DEFAULT 0.0
);
CREATE TABLE "trans" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"customer_id"	INTEGER NOT NULL,
	"unit_price"	NUMERIC NOT NULL DEFAULT 0.00,
	"tax"	NUMERIC NOT NULL DEFAULT 10,
	"misc"	NUMERIC NOT NULL,
	"create_date"	TEXT NOT NULL,
	"final_price"	NUMERIC,
	"status"	TEXT NOT NULL DEFAULT 'ACTIVE',
	"cancel_date"	TEXT,
	"balance"	NUMERIC DEFAULT 0.00
);
CREATE TABLE "transaction_items" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"tx_id"	INTEGER NOT NULL,
	"item_id"	INTEGER NOT NULL,
	"qty"	INTEGER NOT NULL DEFAULT 1,
	"discount"	NUMERIC NOT NULL DEFAULT 0.00,
	"unit_price"	REAL DEFAULT 0.00,
	"other_price"	REAL DEFAULT 0.00,
	"total_price"	REAL DEFAULT 0.00
);
CREATE TABLE "payment" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"tx_id"	INTEGER NOT NULL,
	"amount"	NUMERIC NOT NULL,
	"payment_type"	TEXT NOT NULL,
	"payment_details"	TEXT,
	"payment_date"	TEXT NOT NULL
);
