import 'package:get/get.dart';
import 'package:sheet_project_app/app/data/providers/convert_provider.dart';
import 'package:sheet_project_app/app/data/models/convert_response_model.dart';

class HomeController extends GetxController {
  final ConvertProvider provider = ConvertProvider();

  var youtubeUrl = ''.obs;
  var filename = ''.obs;
  var isLoading = false.obs;
  var result = Rxn<ConvertResponseModel>();

  Future<void> convert() async {
    if (youtubeUrl.value.isEmpty || filename.value.isEmpty) {
      Get.snackbar("오류", "URL과 파일명을 입력해주세요");
      return;
    }

    try {
      isLoading.value = true;
      final response = await provider.convert(youtubeUrl.value, filename.value);
      if (response.statusCode == 200) {
        result.value = ConvertResponseModel.fromJson(response.body);
        Get.snackbar("성공", "변환 완료!");
      } else {
        Get.snackbar("실패", "서버 오류: ${response.statusCode}");
      }
    } catch (e) {
      Get.snackbar("오류", "요청 실패: $e");
    } finally {
      isLoading.value = false;
    }
  }
}
