BEGIN;
--
-- Create model Category
--
CREATE TABLE "clothingstore_category" ("slug" varchar(80) NOT NULL PRIMARY KEY, "name" varchar(80) NOT NULL, "description" text NOT NULL);
--
-- Create model Order
--
CREATE TABLE "clothingstore_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "billing_address" text NOT NULL, "shipping_address" text NOT NULL, "status" varchar(3) NOT NULL, "delivery_fee" decimal NOT NULL, "additional_notes" text NULL, "payment_details" text NOT NULL, "placed_by_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Product
--
CREATE TABLE "clothingstore_product" ("stock_keeping_unit" varchar(255) NOT NULL PRIMARY KEY, "title" varchar(80) NOT NULL, "body" text NOT NULL, "enabled" bool NOT NULL, "units_in_stock" smallint unsigned NOT NULL CHECK ("units_in_stock" >= 0), "unit_cost" decimal NOT NULL, "unit_price" decimal NOT NULL, "category_id" varchar(80) NULL REFERENCES "clothingstore_category" ("slug") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model ProductImage
--
CREATE TABLE "clothingstore_productimage" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "image" varchar(100) NOT NULL, "alternate_text" varchar(255) NOT NULL, "product_id" varchar(255) NOT NULL REFERENCES "clothingstore_product" ("stock_keeping_unit") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model OrderItem
--
CREATE TABLE "clothingstore_orderitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "unit_price" decimal NOT NULL, "quantity" smallint unsigned NOT NULL CHECK ("quantity" >= 0), "order_id" bigint NOT NULL REFERENCES "clothingstore_order" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" varchar(255) NOT NULL REFERENCES "clothingstore_product" ("stock_keeping_unit") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Address
--
CREATE TABLE "clothingstore_address" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "street" text NOT NULL, "city" text NOT NULL, "postal_code" varchar(4) NOT NULL, "province" text NOT NULL, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "clothingstore_order_placed_by_id_dffcf87f" ON "clothingstore_order" ("placed_by_id");
CREATE INDEX "clothingstore_product_category_id_82b35f19" ON "clothingstore_product" ("category_id");
CREATE INDEX "clothingstore_productimage_product_id_cb6d8be1" ON "clothingstore_productimage" ("product_id");
CREATE INDEX "clothingstore_orderitem_order_id_b8986f35" ON "clothingstore_orderitem" ("order_id");
CREATE INDEX "clothingstore_orderitem_product_id_3cf00e55" ON "clothingstore_orderitem" ("product_id");
CREATE INDEX "clothingstore_address_user_id_4ea809c2" ON "clothingstore_address" ("user_id");
COMMIT;
BEGIN;
--
-- Add field placed_on to order
--
CREATE TABLE "new__clothingstore_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "placed_on" datetime NOT NULL, "billing_address" text NOT NULL, "shipping_address" text NOT NULL, "status" varchar(3) NOT NULL, "delivery_fee" decimal NOT NULL, "additional_notes" text NULL, "payment_details" text NOT NULL, "placed_by_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO "new__clothingstore_order" ("id", "billing_address", "shipping_address", "status", "delivery_fee", "additional_notes", "payment_details", "placed_by_id", "placed_on") SELECT "id", "billing_address", "shipping_address", "status", "delivery_fee", "additional_notes", "payment_details", "placed_by_id", '2022-07-25 13:53:24.189407' FROM "clothingstore_order";
DROP TABLE "clothingstore_order";
ALTER TABLE "new__clothingstore_order" RENAME TO "clothingstore_order";
CREATE INDEX "clothingstore_order_placed_by_id_dffcf87f" ON "clothingstore_order" ("placed_by_id");
COMMIT;
BEGIN;
--
-- Add field contact_number to order
--
CREATE TABLE "new__clothingstore_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "contact_number" varchar(13) NOT NULL, "billing_address" text NOT NULL, "shipping_address" text NOT NULL, "status" varchar(3) NOT NULL, "delivery_fee" decimal NOT NULL, "additional_notes" text NULL, "payment_details" text NOT NULL, "placed_by_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "placed_on" datetime NOT NULL);
INSERT INTO "new__clothingstore_order" ("id", "billing_address", "shipping_address", "status", "delivery_fee", "additional_notes", "payment_details", "placed_by_id", "placed_on", "contact_number") SELECT "id", "billing_address", "shipping_address", "status", "delivery_fee", "additional_notes", "payment_details", "placed_by_id", "placed_on", 'N/A' FROM "clothingstore_order";
DROP TABLE "clothingstore_order";
ALTER TABLE "new__clothingstore_order" RENAME TO "clothingstore_order";
CREATE INDEX "clothingstore_order_placed_by_id_dffcf87f" ON "clothingstore_order" ("placed_by_id");
COMMIT;
