import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://192.168.43.126:5000";
  // change if desktop or phone

  static Future<bool> isFirstTime() async {
    final res = await http.get(Uri.parse("$baseUrl/is-first-time"));
    final data = jsonDecode(res.body);
    return data["first_time"];
  }

  static Future<bool> register(
    String name,
    String email,
    String password,
  ) async {
    final res = await http.post(
      Uri.parse("$baseUrl/register"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "full_name": name,
        "email": email,
        "password": password,
      }),
    );
    return res.statusCode == 201;
  }

  static Future<bool> login(String email, String password) async {
    final res = await http.post(
      Uri.parse("$baseUrl/login"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"email": email, "password": password}),
    );
    return res.statusCode == 200;
  }
}
