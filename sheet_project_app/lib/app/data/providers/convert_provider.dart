import 'package:get/get.dart';

class ConvertProvider extends GetConnect {
  final String baseUrl = 'http://127.0.0.1:8000'; // ⚠️ 나중엔 AWS로 교체 예정

  Future<Response> convert(String youtubeUrl, String filename) async {
    final form = FormData({
      'youtube_url': youtubeUrl,
      'filename': filename,
    });

    final response = await post('$baseUrl/convert', form);

    return response;
  }
}
