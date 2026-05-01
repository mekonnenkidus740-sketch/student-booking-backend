// lib/config.dart
class AppConfig {
  static const String backendIp = "192.168.1.28"; // your PC IP
  static const int backendPort = 5000;

  static String get baseUrl => "http://$backendIp:$backendPort";
}
