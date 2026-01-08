-- ============================================
-- COMPLETE DATABASE SETUP FOR BEAUTY STORE
-- Tạo tất cả tables và import dữ liệu mẫu
-- ============================================

-- Drop database if exists and create new
DROP DATABASE IF EXISTS webmypham;
CREATE DATABASE webmypham CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE webmypham;

-- ============================================
-- CREATE TABLES
-- ============================================

-- 1. Users table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    dob DATETIME,
    gender INT,
    access_token TEXT,
    refresh_token TEXT,
    reset_password_token TEXT,
    version INT DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    INDEX idx_email (email),
    INDEX idx_phone (phone_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Roles table
CREATE TABLE roles (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. User_Roles junction table
CREATE TABLE user_roles (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    role_id VARCHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_role (user_id, role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Addresses table
CREATE TABLE addresses (
    id VARCHAR(36) PRIMARY KEY,
    full_name VARCHAR(100),
    phone_number VARCHAR(20),
    province VARCHAR(100),
    district VARCHAR(100),
    ward VARCHAR(100),
    detail VARCHAR(255),
    is_default BOOLEAN DEFAULT FALSE,
    user_id VARCHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Brands table
CREATE TABLE brands (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    slug VARCHAR(100) UNIQUE,
    image_path VARCHAR(255),
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    INDEX idx_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Categories table
CREATE TABLE categories (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    slug VARCHAR(100) UNIQUE,
    image_path VARCHAR(255),
    description TEXT,
    parent_id VARCHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Products table
CREATE TABLE products (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(200),
    brand_id VARCHAR(36),
    category_id VARCHAR(36),
    description VARCHAR(255),
    thumbnail VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Types table (Loại thuộc tính: màu sắc, dung tích...)
CREATE TABLE types (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Type_Values table (Giá trị cụ thể: Đỏ, 50ml...)
CREATE TABLE type_values (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100),
    type_id VARCHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (type_id) REFERENCES types(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. Product_Types table (Biến thể sản phẩm)
CREATE TABLE product_types (
    id VARCHAR(36) PRIMARY KEY,
    product_id VARCHAR(36),
    type_value_id VARCHAR(36),
    image_path VARCHAR(255),
    price FLOAT,
    status VARCHAR(50),
    quantity INT,
    stock INT,
    discount_price FLOAT,
    volume VARCHAR(50),
    ingredients TEXT,
    `usage` VARCHAR(255),
    skin_type VARCHAR(100),
    origin VARCHAR(100),
    sold INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (type_value_id) REFERENCES type_values(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 11. Vouchers table
CREATE TABLE vouchers (
    id VARCHAR(36) PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    discount FLOAT NOT NULL,
    description VARCHAR(255),
    quantity INT NOT NULL,
    min_order_amount FLOAT,
    max_discount FLOAT,
    `limit` INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 12. Orders table
CREATE TABLE orders (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    address_id VARCHAR(36),
    voucher_id VARCHAR(36),
    status VARCHAR(50),
    payment_method VARCHAR(50),
    total_amount FLOAT,
    discount_amount FLOAT,
    final_amount FLOAT,
    note VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (address_id) REFERENCES addresses(id) ON DELETE SET NULL,
    FOREIGN KEY (voucher_id) REFERENCES vouchers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 13. Order_Details table
CREATE TABLE order_details (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36),
    product_type_id VARCHAR(36),
    price FLOAT,
    number INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_type_id) REFERENCES product_types(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 14. Payments table
CREATE TABLE payments (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36),
    method VARCHAR(50),
    status VARCHAR(50),
    transaction_id VARCHAR(100),
    amount FLOAT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 15. Carts table
CREATE TABLE carts (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 16. Cart_Items table
CREATE TABLE cart_items (
    id VARCHAR(36) PRIMARY KEY,
    cart_id VARCHAR(36),
    product_type_id VARCHAR(36),
    quantity INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (product_type_id) REFERENCES product_types(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 17. Wishlists table
CREATE TABLE wishlists (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 18. Wishlist_Items table
CREATE TABLE wishlist_items (
    id VARCHAR(36) PRIMARY KEY,
    wishlist_id VARCHAR(36),
    product_type_id VARCHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (wishlist_id) REFERENCES wishlists(id) ON DELETE CASCADE,
    FOREIGN KEY (product_type_id) REFERENCES product_types(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 19. Reviews table
CREATE TABLE reviews (
    id VARCHAR(36) PRIMARY KEY,
    product_id VARCHAR(36),
    user_id VARCHAR(36),
    rating INT,
    comment VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 20. Review_Medias table
CREATE TABLE review_medias (
    id VARCHAR(36) PRIMARY KEY,
    review_id VARCHAR(36),
    path VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (review_id) REFERENCES reviews(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 21. Conversations table
CREATE TABLE conversations (
    id VARCHAR(36) PRIMARY KEY,
    customer_id VARCHAR(36) NOT NULL,
    admin_id VARCHAR(36),
    last_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_customer (customer_id),
    INDEX idx_admin (admin_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 22. Messages table
CREATE TABLE messages (
    id VARCHAR(36) PRIMARY KEY,
    conversation_id VARCHAR(36),
    sender_id VARCHAR(36),
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 23. Notifications table
CREATE TABLE notifications (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    type VARCHAR(50),
    sender_id VARCHAR(36),
    order_id VARCHAR(36),
    is_global BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 24. User_Notifications table
CREATE TABLE user_notifications (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    notification_id VARCHAR(36),
    is_read BOOLEAN DEFAULT FALSE,
    read_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME,
    created_by VARCHAR(36),
    updated_by VARCHAR(36),
    deleted_by VARCHAR(36),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (notification_id) REFERENCES notifications(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 25. Alembic version table (for migration tracking)
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert current migration version
INSERT INTO alembic_version (version_num) VALUES ('ver10');

-- ============================================
-- INSERT INITIAL DATA
-- ============================================

-- 1. Insert Roles
INSERT INTO roles (id, name, description, created_at, updated_at) VALUES
(UUID(), 'admin', 'Administrator role', NOW(), NOW()),
(UUID(), 'customer', 'Customer role', NOW(), NOW());

-- 2. Insert Admin User (password: admin123)
INSERT INTO users (id, email, password_hash, first_name, last_name, created_at, updated_at) VALUES
('admin-uuid-0000-0000-000000000001', 'admin@beautystore.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVqN4qQzG', 'Admin', 'User', NOW(), NOW());

-- Link admin user to admin role
INSERT INTO user_roles (id, user_id, role_id, created_at, updated_at)
SELECT UUID(), 'admin-uuid-0000-0000-000000000001', id, NOW(), NOW()
FROM roles WHERE name = 'admin';


-- ============================================
-- MOCK DATA FOR TESTING
-- ============================================

-- 1. Tạo Type (Loại thuộc tính)
INSERT INTO types (id, name, created_at, updated_at) VALUES
('a1b2c3d4-1111-4000-8000-000000000001', 'Màu sắc', NOW(), NOW()),
('a1b2c3d4-1111-4000-8000-000000000002', 'Dung tích', NOW(), NOW());

-- 2. Tạo TypeValue (Giá trị cụ thể)
INSERT INTO type_values (id, name, type_id, created_at, updated_at) VALUES
('b2c3d4e5-2222-4000-8000-000000000001', 'Đỏ', 'a1b2c3d4-1111-4000-8000-000000000001', NOW(), NOW()),
('b2c3d4e5-2222-4000-8000-000000000002', 'Hồng', 'a1b2c3d4-1111-4000-8000-000000000001', NOW(), NOW()),
('b2c3d4e5-2222-4000-8000-000000000003', 'Cam', 'a1b2c3d4-1111-4000-8000-000000000001', NOW(), NOW()),
('b2c3d4e5-2222-4000-8000-000000000004', '50ml', 'a1b2c3d4-1111-4000-8000-000000000002', NOW(), NOW()),
('b2c3d4e5-2222-4000-8000-000000000005', '100ml', 'a1b2c3d4-1111-4000-8000-000000000002', NOW(), NOW()),
('b2c3d4e5-2222-4000-8000-000000000006', '200ml', 'a1b2c3d4-1111-4000-8000-000000000002', NOW(), NOW());

-- 3. Tạo Brand
INSERT INTO brands (id, name, slug, description, created_at, updated_at) VALUES
('c3d4e5f6-3333-4000-8000-000000000001', 'Laneige', 'laneige', 'Thương hiệu Hàn Quốc', NOW(), NOW()),
('c3d4e5f6-3333-4000-8000-000000000002', 'Innisfree', 'innisfree', 'Thương hiệu thiên nhiên', NOW(), NOW());

-- 4. Tạo Category
INSERT INTO categories (id, name, slug, description, created_at, updated_at) VALUES
('d4e5f6a7-4444-4000-8000-000000000001', 'Son môi', 'son-moi', 'Các loại son môi', NOW(), NOW()),
('d4e5f6a7-4444-4000-8000-000000000002', 'Dưỡng da', 'duong-da', 'Các sản phẩm chăm sóc da', NOW(), NOW());

-- 5. Tạo Products (6 sản phẩm)
INSERT INTO products (id, name, description, thumbnail, is_active, brand_id, category_id, created_at, updated_at) VALUES
('e5f6a7b8-5555-4000-8000-000000000001', 'Son Môi Laneige Lip Sleeping Mask', 'Son dưỡng môi ban đêm', '/images/laneige-lip.jpg', 1, 'c3d4e5f6-3333-4000-8000-000000000001', 'd4e5f6a7-4444-4000-8000-000000000001', DATE_SUB(NOW(), INTERVAL 30 DAY), NOW()),
('e5f6a7b8-5555-4000-8000-000000000002', 'Kem Dưỡng Innisfree Green Tea', 'Kem dưỡng ẩm từ trà xanh', '/images/innisfree-cream.jpg', 1, 'c3d4e5f6-3333-4000-8000-000000000002', 'd4e5f6a7-4444-4000-8000-000000000002', DATE_SUB(NOW(), INTERVAL 25 DAY), NOW()),
('e5f6a7b8-5555-4000-8000-000000000003', 'Serum Vitamin C Laneige', 'Serum sáng da với vitamin C', '/images/laneige-serum.jpg', 1, 'c3d4e5f6-3333-4000-8000-000000000001', 'd4e5f6a7-4444-4000-8000-000000000002', DATE_SUB(NOW(), INTERVAL 5 DAY), NOW()),
('e5f6a7b8-5555-4000-8000-000000000004', 'Tẩy Trang Innisfree Apple', 'Nước tẩy trang từ táo xanh', '/images/innisfree-cleanser.jpg', 1, 'c3d4e5f6-3333-4000-8000-000000000002', 'd4e5f6a7-4444-4000-8000-000000000002', DATE_SUB(NOW(), INTERVAL 3 DAY), NOW()),
('e5f6a7b8-5555-4000-8000-000000000005', 'Mặt Nạ Innisfree Volcanic', 'Mặt nạ đất sét núi lửa', '/images/innisfree-mask.jpg', 1, 'c3d4e5f6-3333-4000-8000-000000000002', 'd4e5f6a7-4444-4000-8000-000000000002', DATE_SUB(NOW(), INTERVAL 1 DAY), NOW()),
('e5f6a7b8-5555-4000-8000-000000000006', 'Son Dưỡng Laneige Glowy', 'Son dưỡng bóng tự nhiên', '/images/laneige-glowy.jpg', 1, 'c3d4e5f6-3333-4000-8000-000000000001', 'd4e5f6a7-4444-4000-8000-000000000001', NOW(), NOW());

-- 6. Tạo ProductTypes (biến thể)
INSERT INTO product_types (id, product_id, type_value_id, price, discount_price, stock, image_path, volume, origin, skin_type, created_at, updated_at) VALUES
-- Son Laneige Lip Sleeping Mask - 3 màu
('f6a7b8c9-6666-4000-8000-000000000001', 'e5f6a7b8-5555-4000-8000-000000000001', 'b2c3d4e5-2222-4000-8000-000000000001', 350000, 299000, 30, '/images/laneige-red.jpg', '8g', 'Hàn Quốc', 'Mọi loại da', NOW(), NOW()),
('f6a7b8c9-6666-4000-8000-000000000002', 'e5f6a7b8-5555-4000-8000-000000000001', 'b2c3d4e5-2222-4000-8000-000000000002', 350000, 299000, 25, '/images/laneige-pink.jpg', '8g', 'Hàn Quốc', 'Mọi loại da', NOW(), NOW()),
('f6a7b8c9-6666-4000-8000-000000000003', 'e5f6a7b8-5555-4000-8000-000000000001', 'b2c3d4e5-2222-4000-8000-000000000003', 350000, 299000, 0, '/images/laneige-orange.jpg', '8g', 'Hàn Quốc', 'Mọi loại da', NOW(), NOW()),
-- Kem Innisfree - 3 dung tích
('f6a7b8c9-6666-4000-8000-000000000004', 'e5f6a7b8-5555-4000-8000-000000000002', 'b2c3d4e5-2222-4000-8000-000000000004', 450000, 399000, 50, '/images/innisfree-50.jpg', '50ml', 'Hàn Quốc', 'Da khô', NOW(), NOW()),
('f6a7b8c9-6666-4000-8000-000000000005', 'e5f6a7b8-5555-4000-8000-000000000002', 'b2c3d4e5-2222-4000-8000-000000000005', 750000, 650000, 20, '/images/innisfree-100.jpg', '100ml', 'Hàn Quốc', 'Da khô', NOW(), NOW()),
('f6a7b8c9-6666-4000-8000-000000000006', 'e5f6a7b8-5555-4000-8000-000000000002', 'b2c3d4e5-2222-4000-8000-000000000006', 1200000, 999000, 10, '/images/innisfree-200.jpg', '200ml', 'Hàn Quốc', 'Da khô', NOW(), NOW()),
-- Serum, Tẩy trang, Mặt nạ, Son Glowy
('f6a7b8c9-6666-4000-8000-000000000007', 'e5f6a7b8-5555-4000-8000-000000000003', NULL, 890000, 750000, 40, '/images/laneige-serum.jpg', '30ml', 'Hàn Quốc', 'Mọi loại da', NOW(), NOW()),
('f6a7b8c9-6666-4000-8000-000000000008', 'e5f6a7b8-5555-4000-8000-000000000004', NULL, 320000, 280000, 60, '/images/innisfree-cleanser.jpg', '150ml', 'Hàn Quốc', 'Mọi loại da', NOW(), NOW()),
('f6a7b8c9-6666-4000-8000-000000000009', 'e5f6a7b8-5555-4000-8000-000000000005', NULL, 250000, 199000, 100, '/images/innisfree-mask.jpg', '100ml', 'Hàn Quốc', 'Da dầu', NOW(), NOW()),
('f6a7b8c9-6666-4000-8000-000000000010', 'e5f6a7b8-5555-4000-8000-000000000006', NULL, 380000, 320000, 45, '/images/laneige-glowy.jpg', '10g', 'Hàn Quốc', 'Mọi loại da', NOW(), NOW());

-- 7. Tạo Vouchers
INSERT INTO vouchers (id, code, discount, description, quantity, min_order_amount, max_discount, `limit`, created_at, updated_at) VALUES
('v1v1v1v1-7777-4000-8000-000000000001', 'WELCOME10', 10, 'Giảm 10% cho đơn hàng đầu tiên', 100, 200000, 50000, 1, NOW(), NOW()),
('v2v2v2v2-7777-4000-8000-000000000002', 'SUMMER20', 20, 'Giảm 20% mùa hè', 50, 500000, 100000, NULL, NOW(), NOW());

-- 8. Tạo Test Customer (password: customer123)
INSERT INTO users (id, email, password_hash, first_name, last_name, phone_number, created_at, updated_at) VALUES
('customer-uuid-0000-0000-000000000001', 'customer@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVqN4qQzG', 'Test', 'Customer', '0123456789', NOW(), NOW());

-- Link customer to customer role
INSERT INTO user_roles (id, user_id, role_id, created_at, updated_at)
SELECT UUID(), 'customer-uuid-0000-0000-000000000001', id, NOW(), NOW()
FROM roles WHERE name = 'customer';

-- ============================================
-- SETUP COMPLETE!
-- ============================================
-- Database: webmypham
-- Admin: admin@beautystore.com / admin123
-- Customer: customer@test.com / customer123
-- ============================================
