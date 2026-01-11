import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from datetime import datetime
from app.core.config import settings


class EmailService:
    """Service để gửi email sử dụng SMTP"""

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        body_html: str,
        body_text: Optional[str] = None
    ) -> bool:
        """
        Gửi email với HTML content
        
        Args:
            to_email: Email người nhận
            subject: Tiêu đề email
            body_html: Nội dung HTML
            body_text: Nội dung text thuần (fallback)
            
        Returns:
            True nếu gửi thành công, False nếu thất bại
        """
        try:
            # Tạo message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            # Thêm plain text (fallback)
            if body_text:
                part1 = MIMEText(body_text, 'plain', 'utf-8')
                msg.attach(part1)

            # Thêm HTML
            part2 = MIMEText(body_html, 'html', 'utf-8')
            msg.attach(part2)

            # Kết nối SMTP server
            if settings.SMTP_USE_SSL:
                server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
            else:
                server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
                if settings.SMTP_USE_TLS:
                    server.starttls()

            # Login và gửi email
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()

            return True

        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    @staticmethod
    def send_verification_code(to_email: str, code: str, user_name: Optional[str] = None) -> bool:
        """
        Gửi mã xác thực 6 số qua email
        
        Args:
            to_email: Email người nhận
            code: Mã 6 số
            user_name: Tên người dùng (nếu có)
            
        Returns:
            True nếu gửi thành công
        """
        subject = "Mã xác thực tài khoản - WebMyPham"
        
        name_display = user_name if user_name else "bạn"
        
        # HTML Template
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .container {{
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    color: #e91e63;
                    margin-bottom: 20px;
                }}
                .code-box {{
                    background-color: #fff;
                    border: 2px dashed #e91e63;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    margin: 30px 0;
                }}
                .code {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #e91e63;
                    letter-spacing: 8px;
                    font-family: 'Courier New', monospace;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 12px;
                    margin: 20px 0;
                    font-size: 14px;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="header">🔐 Xác Thực Tài Khoản</h1>
                <p>Xin chào <strong>{name_display}</strong>,</p>
                <p>Cảm ơn bạn đã đăng ký tài khoản tại <strong>WebMyPham</strong>. Để hoàn tất quá trình đăng ký, vui lòng sử dụng mã xác thực bên dưới:</p>
                
                <div class="code-box">
                    <div class="code">{code}</div>
                </div>
                
                <div class="warning">
                    ⚠️ <strong>Lưu ý:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px;">
                        <li>Mã này có hiệu lực trong <strong>10 phút</strong></li>
                        <li>Không chia sẻ mã này với bất kỳ ai</li>
                        <li>Nếu bạn không yêu cầu mã này, vui lòng bỏ qua email</li>
                    </ul>
                </div>
                
                <p>Trân trọng,<br><strong>Đội ngũ WebMyPham</strong></p>
                
                <div class="footer">
                    <p>Email này được gửi tự động, vui lòng không trả lời.</p>
                    <p>&copy; 2026 WebMyPham. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        text_body = f"""
        Xác Thực Tài Khoản - WebMyPham
        
        Xin chào {name_display},
        
        Mã xác thực của bạn là: {code}
        
        Mã này có hiệu lực trong 10 phút.
        Không chia sẻ mã này với bất kỳ ai.
        
        Trân trọng,
        Đội ngũ WebMyPham
        """
        
        return EmailService.send_email(to_email, subject, html_body, text_body)

    @staticmethod
    def send_reset_password_by_admin(
        to_email: str, 
        new_password: str, 
        user_name: Optional[str] = None
    ) -> bool:
        """
        Gửi email thông báo mật khẩu mới sau khi Admin reset.
        
        Args:
            to_email: Email người nhận
            new_password: Mật khẩu mới
            user_name: Tên người dùng (nếu có)
            
        Returns:
            True nếu gửi thành công
        """
        subject = "Mật khẩu của bạn đã được reset - WebMyPham"
        
        name_display = user_name if user_name else "bạn"
        
        # HTML Template
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .container {{
                    background-color: #f9f9f9;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    color: #e91e63;
                    margin-bottom: 20px;
                }}
                .info-box {{
                    background-color: #fff;
                    border-left: 4px solid #e91e63;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
                .info-row {{
                    display: flex;
                    margin: 10px 0;
                    font-size: 14px;
                }}
                .info-label {{
                    font-weight: bold;
                    width: 120px;
                    color: #666;
                }}
                .info-value {{
                    color: #333;
                    font-family: 'Courier New', monospace;
                }}
                .password-box {{
                    background-color: #fff;
                    border: 2px dashed #e91e63;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    margin: 30px 0;
                }}
                .password {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #e91e63;
                    letter-spacing: 2px;
                    font-family: 'Courier New', monospace;
                    word-break: break-all;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 12px;
                    margin: 20px 0;
                    font-size: 14px;
                }}
                .action-box {{
                    background-color: #e3f2fd;
                    border-left: 4px solid #2196f3;
                    padding: 15px;
                    margin: 20px 0;
                    font-size: 14px;
                }}
                .footer {{
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #666;
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="header">🔑 Mật Khẩu Đã Được Reset</h1>
                <p>Xin chào <strong>{name_display}</strong>,</p>
                <p>Mật khẩu tài khoản của bạn tại <strong>WebMyPham</strong> đã được quản trị viên reset thành công.</p>
                
                <div class="info-box">
                    <div class="info-row">
                        <div class="info-label">Tài khoản:</div>
                        <div class="info-value">{to_email}</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Thời gian:</div>
                        <div class="info-value">{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
                    </div>
                </div>
                
                <p style="margin-top: 20px;">Mật khẩu mới của bạn là:</p>
                <div class="password-box">
                    <div class="password">{new_password}</div>
                </div>
                
                <div class="warning">
                    ⚠️ <strong>Lưu ý bảo mật:</strong>
                    <ul style="margin: 5px 0; padding-left: 20px;">
                        <li>Vui lòng <strong>đổi mật khẩu ngay</strong> sau khi đăng nhập</li>
                        <li>Không chia sẻ mật khẩu này với bất kỳ ai</li>
                        <li>Chọn mật khẩu mới mạnh và dễ nhớ</li>
                    </ul>
                </div>
                
                <div class="action-box">
                    ℹ️ <strong>Hướng dẫn đổi mật khẩu:</strong>
                    <ol style="margin: 5px 0; padding-left: 20px;">
                        <li>Đăng nhập bằng mật khẩu trên</li>
                        <li>Vào <strong>Tài khoản</strong> → <strong>Bảo mật</strong></li>
                        <li>Chọn <strong>Đổi mật khẩu</strong></li>
                        <li>Nhập mật khẩu mới và xác nhận</li>
                    </ol>
                </div>
                
                <p>Nếu bạn không yêu cầu reset mật khẩu, vui lòng liên hệ bộ phận hỗ trợ ngay lập tức.</p>
                
                <p>Trân trọng,<br><strong>Đội ngũ WebMyPham</strong></p>
                
                <div class="footer">
                    <p>Email này được gửi tự động, vui lòng không trả lời.</p>
                    <p>Nếu cần hỗ trợ, vui lòng liên hệ: support@webmypham.com</p>
                    <p>&copy; 2026 WebMyPham. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text fallback
        text_body = f"""
        Mật Khẩu Đã Được Reset - WebMyPham
        
        Xin chào {name_display},
        
        Mật khẩu tài khoản của bạn đã được quản trị viên reset.
        
        Tài khoản: {to_email}
        Mật khẩu mới: {new_password}
        
        VUI LÒNG ĐỔI MẬT KHẨU NGAY SAU KHI ĐĂNG NHẬP!
        
        Nếu bạn không yêu cầu reset mật khẩu, vui lòng liên hệ bộ phận hỗ trợ ngay.
        
        Trân trọng,
        Đội ngũ WebMyPham
        """
        
        return EmailService.send_email(to_email, subject, html_body, text_body)
