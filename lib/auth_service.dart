import 'dart:convert';
import 'package:http/http.dart' as http;
import 'api.dart';

class AuthService {
  // Regular student registration
  static Future<bool> registerStudent({
    required String firstName,
    required String lastName,
    String? phone,
  }) async {
    final url = Uri.parse("${Api.baseUrl}/register");
    final body = jsonEncode({
      "first_name": firstName,
      "last_name": lastName,
      "phone": phone ?? "",
    });

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: body,
      );

      return response.statusCode == 201;
    } catch (e) {
      print("Registration error: $e");
      return false;
    }
  }

  // Google user registration
  static Future<bool> registerGoogleUser({
    required String email,
    required String firstName,
    required String lastName,
  }) async {
    final url = Uri.parse("${Api.baseUrl}/register_google");
    final body = jsonEncode({
      "email": email,
      "first_name": firstName,
      "last_name": lastName,
    });

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: body,
      );

      return response.statusCode == 201;
    } catch (e) {
      print("Google registration error: $e");
      return false;
    }
  }

  // Check if Google user already exists
  static Future<bool> checkGoogleUserExists(String email) async {
    final url = Uri.parse("${Api.baseUrl}/check_google_user?email=$email");
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['exists'] ?? false;
      }
      return false;
    } catch (e) {
      print("Check Google user error: $e");
      return false;
    }
  }
}
