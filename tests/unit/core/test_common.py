"""Comprehensive unit tests for ultimate_rvc.core.common module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import json
import math
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from ultimate_rvc.core.common import (
    AUDIO_DIR,
    FLAG_FILE,
    INTERMEDIATE_AUDIO_BASE_DIR,
    MODELS_DIR,
    OUTPUT_AUDIO_DIR,
    SPEECH_DIR,
    TRAINING_AUDIO_DIR,
    copy_file_safe,
    copy_files_to_new_dir,
    display_progress,
    get_combined_file_hash,
    get_file_hash,
    get_file_size,
    get_hash,
    json_dump,
    json_dumps,
    json_load,
    remove_suffix_after,
    validate_audio_dir_exists,
    validate_audio_file_exists,
    validate_model,
    validate_url,
)
from ultimate_rvc.core.exceptions import (
    AudioFileEntity,
    Entity,
    HttpUrlError,
    ModelEntity,
    ModelExistsError,
    ModelNotFoundError,
    NotFoundError,
    NotProvidedError,
    UIMessage,
)

if TYPE_CHECKING:
    from typing import Any

    import pytest_mock


# Constants for hash sizes in hex characters (bytes * 2)
DEFAULT_HASH_SIZE = 10  # 5 bytes * 2
SMALL_HASH_SIZE = 6  # 3 bytes * 2
LARGE_HASH_SIZE = 20  # 10 bytes * 2

# Constants for test file sizes
EXPECTED_FILE_SIZE = 1024
EXPECTED_LARGE_FILE_SIZE = 2048


class TestConstants:
    """Test that module constants are correctly defined."""

    def test_directory_constants_are_paths(self) -> None:
        """Test that all directory constants are Path objects."""
        constants = [
            INTERMEDIATE_AUDIO_BASE_DIR,
            SPEECH_DIR,
            OUTPUT_AUDIO_DIR,
            FLAG_FILE,
            TRAINING_AUDIO_DIR,
        ]
        for constant in constants:
            assert isinstance(constant, Path)

    def test_directory_constants_are_subdirs_of_base_dirs(self) -> None:
        """Test that directory constants are proper subdirectories."""
        assert INTERMEDIATE_AUDIO_BASE_DIR.parent == AUDIO_DIR
        assert SPEECH_DIR.parent == AUDIO_DIR
        assert OUTPUT_AUDIO_DIR.parent == AUDIO_DIR
        assert TRAINING_AUDIO_DIR.parent == AUDIO_DIR
        assert FLAG_FILE.parent == MODELS_DIR


class TestDisplayProgress:
    """Test cases for display_progress function."""

    def test_display_progress_with_message_only(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test display_progress with only message parameter."""
        message = "Processing audio file..."
        display_progress(message)

        captured = capsys.readouterr()
        assert message in captured.out

    def test_display_progress_with_percentage(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test display_progress with message and percentage."""
        message = "Training model..."
        percentage = 45.5
        display_progress(message, percentage)

        captured = capsys.readouterr()
        assert message in captured.out

    def test_display_progress_with_gradio_progress_bar(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test display_progress with Gradio progress bar."""
        message = "Converting voice..."
        percentage = 75.0
        mock_progress_bar = MagicMock()

        display_progress(message, percentage, mock_progress_bar)

        captured = capsys.readouterr()
        assert message in captured.out
        mock_progress_bar.assert_called_once_with(percentage, desc=message)

    def test_display_progress_with_none_percentage(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test display_progress with None percentage."""
        message = "Initializing..."
        mock_progress_bar = MagicMock()

        display_progress(message, None, mock_progress_bar)

        captured = capsys.readouterr()
        assert message in captured.out
        mock_progress_bar.assert_called_once_with(None, desc=message)

    @pytest.mark.parametrize(
        ("message", "percentage"),
        [
            ("", 0.0),
            ("Test message", 0.0),
            ("Another test", 100.0),
            ("Unicode test 🎵", 50.0),
            ("Moderately long message test", 25.5),
        ],
    )
    def test_display_progress_parametrized(
        self, message: str, percentage: float, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """
        Test display_progress with various message and percentage
        combinations.
        """
        display_progress(message, percentage)

        captured = capsys.readouterr()
        assert message in captured.out


class TestRemoveSuffixAfter:
    """Test cases for remove_suffix_after function."""

    def test_remove_suffix_after_basic(self) -> None:
        """Test basic functionality of remove_suffix_after."""
        text = "hello_world_test.txt"
        occurrence = "_world"
        expected = "hello_world"

        result = remove_suffix_after(text, occurrence)
        assert result == expected

    def test_remove_suffix_after_not_found(self) -> None:
        """Test remove_suffix_after when occurrence is not found."""
        text = "hello_world.txt"
        occurrence = "_missing"

        result = remove_suffix_after(text, occurrence)
        assert result == text  # Should return original text

    def test_remove_suffix_after_multiple_occurrences(self) -> None:
        """
        Test remove_suffix_after with multiple occurrences
        (uses rightmost).
        """
        text = "test_file_name_test_suffix.wav"
        occurrence = "_test"
        expected = "test_file_name_test"

        result = remove_suffix_after(text, occurrence)
        assert result == expected

    def test_remove_suffix_after_empty_strings(self) -> None:
        """Test remove_suffix_after with empty strings."""
        assert not remove_suffix_after("", "")
        assert remove_suffix_after("test", "") == "test"
        assert not remove_suffix_after("", "test")

    def test_remove_suffix_after_occurrence_at_end(self) -> None:
        """Test remove_suffix_after when occurrence is at the end."""
        text = "filename.txt"
        occurrence = ".txt"
        expected = "filename.txt"  # Keeps everything including the occurrence

        result = remove_suffix_after(text, occurrence)
        assert result == expected

    @pytest.mark.parametrize(
        ("text", "occurrence", "expected"),
        [
            ("file.mp3", ".mp3", "file.mp3"),  # Keeps everything including occurrence
            ("audio_track_v1.2.wav", "_v1", "audio_track_v1"),
            ("model_weights.pth", ".pth", "model_weights.pth"),
            (
                "test__double__underscore",
                "__",
                "test__double__",
            ),  # Uses rightmost occurrence
            ("no_match_here", "xyz", "no_match_here"),
            ("case_SensITive", "sensitive", "case_SensITive"),  # Case sensitive
            ("case_SensITive", "SensI", "case_SensI"),
        ],
    )
    def test_remove_suffix_after_parametrized(
        self, text: str, occurrence: str, expected: str
    ) -> None:
        """Test remove_suffix_after with various inputs."""
        result = remove_suffix_after(text, occurrence)
        assert result == expected


class TestCopyFilesToNewDir:
    """Test cases for copy_files_to_new_dir function."""

    def test_copy_files_to_new_dir_success(self, tmp_path: Path) -> None:
        """Test successful copying of files to new directory."""
        # Create source files
        source_dir = tmp_path / "source"
        source_dir.mkdir()
        file1 = source_dir / "file1.txt"
        file2 = source_dir / "file2.wav"
        file1.write_text("content1")
        file2.write_text("content2")

        # Create destination directory
        dest_dir = tmp_path / "destination"

        # Copy files
        copy_files_to_new_dir([file1, file2], dest_dir)

        # Verify files were copied
        assert (dest_dir / "file1.txt").exists()
        assert (dest_dir / "file2.wav").exists()
        assert (dest_dir / "file1.txt").read_text() == "content1"
        assert (dest_dir / "file2.wav").read_text() == "content2"

    def test_copy_files_to_new_dir_creates_parent_dirs(self, tmp_path: Path) -> None:
        """
        Test that parent directories are created if they don't
        exist.
        """
        # Create source file
        source_file = tmp_path / "source.txt"
        source_file.write_text("test content")

        # Use nested destination directory
        dest_dir = tmp_path / "nested" / "deep" / "directory"

        copy_files_to_new_dir([source_file], dest_dir)

        assert dest_dir.exists()
        assert (dest_dir / "source.txt").exists()

    def test_copy_files_to_new_dir_file_not_found(self, tmp_path: Path) -> None:
        """Test copy_files_to_new_dir with non-existent file."""
        nonexistent_file = tmp_path / "nonexistent.txt"
        dest_dir = tmp_path / "destination"

        with pytest.raises(NotFoundError) as exc_info:
            copy_files_to_new_dir([nonexistent_file], dest_dir)

        error_message = str(exc_info.value)
        assert "File not found" in error_message
        assert str(nonexistent_file) in error_message

    def test_copy_files_to_new_dir_empty_file_list(self, tmp_path: Path) -> None:
        """Test copy_files_to_new_dir with empty file list."""
        dest_dir = tmp_path / "destination"

        copy_files_to_new_dir([], dest_dir)

        assert dest_dir.exists()
        assert list(dest_dir.iterdir()) == []

    def test_copy_files_to_new_dir_with_path_objects(self, tmp_path: Path) -> None:
        """Test copy_files_to_new_dir with Path objects."""
        source_file = tmp_path / "source.txt"
        source_file.write_text("test")
        dest_dir = tmp_path / "dest"

        copy_files_to_new_dir([source_file], dest_dir)

        assert (dest_dir / "source.txt").exists()

    def test_copy_files_to_new_dir_with_string_paths(self, tmp_path: Path) -> None:
        """Test copy_files_to_new_dir with string paths."""
        source_file = tmp_path / "source.txt"
        source_file.write_text("test")
        dest_dir = tmp_path / "dest"

        copy_files_to_new_dir([str(source_file)], str(dest_dir))

        assert (dest_dir / "source.txt").exists()


class TestCopyFileSafe:
    """Test cases for copy_file_safe function."""

    def test_copy_file_safe_no_collision(self, tmp_path: Path) -> None:
        """Test copy_file_safe when destination doesn't exist."""
        source = tmp_path / "source.txt"
        source.write_text("test content")
        dest = tmp_path / "dest.txt"

        result = copy_file_safe(source, dest)

        assert result == dest
        assert result.exists()
        assert result.read_text() == "test content"

    def test_copy_file_safe_with_collision(self, tmp_path: Path) -> None:
        """Test copy_file_safe when destination already exists."""
        source = tmp_path / "source.txt"
        source.write_text("new content")
        dest = tmp_path / "dest.txt"
        dest.write_text("existing content")

        result = copy_file_safe(source, dest)

        expected = tmp_path / "dest (1).txt"
        assert result == expected
        assert result.exists()
        assert result.read_text() == "new content"
        assert dest.read_text() == "existing content"  # Original unchanged

    def test_copy_file_safe_multiple_collisions(self, tmp_path: Path) -> None:
        """Test copy_file_safe with multiple existing files."""
        source = tmp_path / "source.wav"
        source.write_text("audio data")

        # Create existing files
        dest = tmp_path / "dest.wav"
        dest.write_text("existing")
        (tmp_path / "dest (1).wav").write_text("existing1")
        (tmp_path / "dest (2).wav").write_text("existing2")

        result = copy_file_safe(source, dest)

        expected = tmp_path / "dest (3).wav"
        assert result == expected
        assert result.exists()
        assert result.read_text() == "audio data"

    def test_copy_file_safe_creates_parent_dirs(self, tmp_path: Path) -> None:
        """Test copy_file_safe creates parent directories."""
        source = tmp_path / "source.txt"
        source.write_text("test")
        dest = tmp_path / "nested" / "deep" / "dest.txt"

        result = copy_file_safe(source, dest)

        assert result == dest
        assert result.exists()
        assert dest.parent.exists()

    def test_copy_file_safe_preserves_extension(self, tmp_path: Path) -> None:
        """
        Test copy_file_safe preserves destination extension in renamed
        files.
        """
        source = tmp_path / "source.complex.ext.name"
        source.write_text("test")
        dest = tmp_path / "dest.simple.ext"
        dest.write_text("existing")

        result = copy_file_safe(source, dest)

        expected = tmp_path / "dest.simple (1).ext"
        assert result == expected
        assert result.exists()

    @pytest.mark.parametrize(
        ("filename", "extension"),
        [
            ("test", ".txt"),
            ("audio", ".wav"),
            ("model", ".pth"),
            ("config", ".json"),
            ("data", ".csv"),
        ],
    )
    def test_copy_file_safe_different_extensions(
        self, tmp_path: Path, filename: str, extension: str
    ) -> None:
        """Test copy_file_safe with different file extensions."""
        source = tmp_path / f"{filename}{extension}"
        source.write_text("content")
        dest = tmp_path / f"dest{extension}"

        result = copy_file_safe(source, dest)

        assert result == dest
        assert result.suffix == extension


class TestJsonOperations:
    """Test cases for JSON serialization/deserialization functions."""

    def test_json_dumps_basic(self) -> None:
        """Test json_dumps with basic data types."""
        data = {"name": "test", "value": 42, "active": True}
        result = json_dumps(data)

        assert isinstance(result, str)
        parsed = json.loads(result)
        assert parsed == data

    def test_json_dumps_formatting(self) -> None:
        """Test json_dumps produces properly formatted output."""
        data = {"key": "value"}
        result = json_dumps(data)

        # Should have indentation (4 spaces)
        assert "    " in result
        # Should preserve unicode
        assert "value" in result

    def test_json_dumps_unicode(self) -> None:
        """Test json_dumps with unicode characters."""
        data = {"message": "Hello 世界 🎵", "emoji": "🎤"}
        result = json_dumps(data)

        # Should preserve unicode characters
        assert "世界" in result
        assert "🎵" in result
        assert "🎤" in result

    def test_json_dump_creates_file(self, tmp_path: Path) -> None:
        """Test json_dump creates JSON file."""
        data = {"test": "data", "number": 123}
        file_path = tmp_path / "test.json"

        json_dump(data, file_path)

        assert file_path.exists()
        loaded_data = json.loads(file_path.read_text(encoding="utf-8"))
        assert loaded_data == data

    def test_json_dump_overwrites_existing(self, tmp_path: Path) -> None:
        """Test json_dump overwrites existing file."""
        file_path = tmp_path / "test.json"
        file_path.write_text('{"old": "data"}')

        new_data = {"new": "data"}
        json_dump(new_data, file_path)

        loaded_data = json.loads(file_path.read_text(encoding="utf-8"))
        assert loaded_data == new_data

    def test_json_load_basic(self, tmp_path: Path) -> None:
        """Test json_load reads JSON file correctly."""
        data = {"config": {"sample_rate": 44100, "channels": 2}}
        file_path = tmp_path / "config.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        result = json_load(file_path)

        assert result == data

    def test_json_load_different_encoding(self, tmp_path: Path) -> None:
        """Test json_load with different encoding."""
        data = {"message": "café"}
        file_path = tmp_path / "test.json"

        # Write with latin-1 encoding
        with file_path.open("w", encoding="latin-1") as f:
            json.dump(data, f, ensure_ascii=False)

        result = json_load(file_path, encoding="latin-1")
        assert result == data

    @pytest.mark.parametrize(
        "data",
        [
            {},
            {"simple": "value"},
            {"nested": {"key": "value", "number": 42}},
            {"list": [1, 2, 3]},
            {
                "mixed": {
                    "string": "test",
                    "int": 1,
                    "float": math.pi,
                    "bool": True,
                    "null": None,
                }
            },
            {"unicode": "Hello 世界 🎵"},
        ],
    )
    def test_json_round_trip(self, tmp_path: Path, data: dict[str, Any]) -> None:
        """Test JSON dump/load round trip preserves data."""
        file_path = tmp_path / "roundtrip.json"

        json_dump(data, file_path)
        result = json_load(file_path)

        assert result == data


class TestHashFunctions:
    """Test cases for hashing functions."""

    def test_get_hash_deterministic(self) -> None:
        """Test get_hash produces deterministic results."""
        data = {"key": "value", "number": 42}

        hash1 = get_hash(data)
        hash2 = get_hash(data)

        assert hash1 == hash2
        assert isinstance(hash1, str)
        assert len(hash1) == DEFAULT_HASH_SIZE

    def test_get_hash_different_data(self) -> None:
        """
        Test get_hash produces different hashes for different
        data.
        """
        data1 = {"key": "value1"}
        data2 = {"key": "value2"}

        hash1 = get_hash(data1)
        hash2 = get_hash(data2)

        assert hash1 != hash2

    def test_get_hash_custom_size(self) -> None:
        """Test get_hash with custom hash size."""
        data = {"test": "data"}

        hash_small = get_hash(data, size=3)
        hash_large = get_hash(data, size=10)

        assert len(hash_small) == SMALL_HASH_SIZE
        assert len(hash_large) == LARGE_HASH_SIZE

    def test_get_file_hash_basic(self, tmp_path: Path) -> None:
        """Test get_file_hash with basic file."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")

        hash_result = get_file_hash(file_path)

        assert isinstance(hash_result, str)
        assert len(hash_result) == DEFAULT_HASH_SIZE

    def test_get_file_hash_deterministic(self, tmp_path: Path) -> None:
        """Test get_file_hash is deterministic."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("consistent content")

        hash1 = get_file_hash(file_path)
        hash2 = get_file_hash(file_path)

        assert hash1 == hash2

    def test_get_file_hash_different_content(self, tmp_path: Path) -> None:
        """
        Test get_file_hash produces different hashes for different
        content.
        """
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content1")
        file2.write_text("content2")

        hash1 = get_file_hash(file1)
        hash2 = get_file_hash(file2)

        assert hash1 != hash2

    def test_get_file_hash_binary_file(self, tmp_path: Path) -> None:
        """Test get_file_hash with binary file."""
        file_path = tmp_path / "binary.dat"
        file_path.write_bytes(b"\x00\x01\x02\x03\xff")

        hash_result = get_file_hash(file_path)

        assert isinstance(hash_result, str)
        assert len(hash_result) == DEFAULT_HASH_SIZE

    def test_get_combined_file_hash_basic(self, tmp_path: Path) -> None:
        """Test get_combined_file_hash with multiple files."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content1")
        file2.write_text("content2")

        combined_hash = get_combined_file_hash([file1, file2])

        assert isinstance(combined_hash, str)
        assert len(combined_hash) == DEFAULT_HASH_SIZE

    def test_get_combined_file_hash_order_matters(self, tmp_path: Path) -> None:
        """Test get_combined_file_hash is sensitive to file order."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"
        file1.write_text("content1")
        file2.write_text("content2")

        hash_order1 = get_combined_file_hash([file1, file2])
        hash_order2 = get_combined_file_hash([file2, file1])

        assert hash_order1 != hash_order2

    def test_get_combined_file_hash_single_file(self, tmp_path: Path) -> None:
        """Test get_combined_file_hash with single file."""
        file_path = tmp_path / "single.txt"
        file_path.write_text("single file content")

        combined_hash = get_combined_file_hash([file_path])
        individual_hash = get_file_hash(file_path)

        # Both should be valid hash strings
        assert isinstance(combined_hash, str)
        assert isinstance(individual_hash, str)
        assert len(combined_hash) == DEFAULT_HASH_SIZE
        assert len(individual_hash) == DEFAULT_HASH_SIZE
        # They might be the same or different depending on
        # implementation

    def test_get_combined_file_hash_empty_list(self) -> None:
        """Test get_combined_file_hash with empty file list."""
        combined_hash = get_combined_file_hash([])

        assert isinstance(combined_hash, str)
        assert len(combined_hash) == DEFAULT_HASH_SIZE

    @pytest.mark.parametrize("size", [1, 3, 5, 8, 16, 32])
    def test_hash_functions_custom_sizes(self, tmp_path: Path, size: int) -> None:
        """Test hash functions with various sizes."""
        data = {"test": "data"}
        file_path = tmp_path / "test.txt"
        file_path.write_text("test content")

        hash_json = get_hash(data, size=size)
        hash_file = get_file_hash(file_path, size=size)
        hash_combined = get_combined_file_hash([file_path], size=size)

        expected_length = size * 2  # size bytes * 2 (hex)
        assert len(hash_json) == expected_length
        assert len(hash_file) == expected_length
        assert len(hash_combined) == expected_length


class TestGetFileSize:
    """Test cases for get_file_size function."""

    # Constants for test file sizes
    EXPECTED_FILE_SIZE = 1024
    EXPECTED_LARGE_FILE_SIZE = 2048

    @pytest.mark.network
    def test_get_file_size_success(self, mocker: pytest_mock.MockerFixture) -> None:
        """Test get_file_size with successful HTTP response."""
        mock_response = mocker.MagicMock()
        mock_response.headers = {"content-length": str(EXPECTED_FILE_SIZE)}
        mock_requests = mocker.patch("ultimate_rvc.core.common.requests")
        mock_requests.head.return_value = mock_response

        result = get_file_size("https://example.com/file.zip")

        assert result == EXPECTED_FILE_SIZE
        mock_requests.head.assert_called_once_with(
            "https://example.com/file.zip", timeout=10
        )

    @pytest.mark.network
    def test_get_file_size_no_content_length(
        self, mocker: pytest_mock.MockerFixture
    ) -> None:
        """Test get_file_size when content-length header is missing."""
        mock_response = mocker.MagicMock()
        mock_response.headers = {}
        mock_requests = mocker.patch("ultimate_rvc.core.common.requests")
        mock_requests.head.return_value = mock_response

        result = get_file_size("https://example.com/file.zip")

        assert result == 0

    @pytest.mark.network
    def test_get_file_size_empty_file(self, mocker: pytest_mock.MockerFixture) -> None:
        """Test get_file_size with empty file (content-length: 0)."""
        mock_response = mocker.MagicMock()
        mock_response.headers = {"content-length": "0"}
        mock_requests = mocker.patch("ultimate_rvc.core.common.requests")
        mock_requests.head.return_value = mock_response

        result = get_file_size("https://example.com/empty.txt")

        assert result == 0  # Empty file should return 0, not None

    @pytest.mark.network
    def test_get_file_size_http_error(self, mocker: pytest_mock.MockerFixture) -> None:
        """Test get_file_size with HTTP error."""
        mock_requests = mocker.patch("ultimate_rvc.core.common.requests")
        mock_requests.head.side_effect = Exception("HTTP Error")

        with pytest.raises(Exception, match="HTTP Error"):
            get_file_size("https://example.com/nonexistent.zip")

    @pytest.mark.network
    def test_get_file_size_timeout(self, mocker: pytest_mock.MockerFixture) -> None:
        """Test get_file_size uses correct timeout."""
        mock_response = mocker.MagicMock()
        mock_response.headers = {"content-length": str(EXPECTED_LARGE_FILE_SIZE)}
        mock_requests = mocker.patch("ultimate_rvc.core.common.requests")
        mock_requests.head.return_value = mock_response

        get_file_size("https://example.com/large_file.zip")

        mock_requests.head.assert_called_with(
            "https://example.com/large_file.zip", timeout=10
        )


class TestValidateAudioFileExists:
    """Test cases for validate_audio_file_exists function."""

    def test_validate_audio_file_exists_success(self, tmp_path: Path) -> None:
        """Test validate_audio_file_exists with existing file."""
        audio_file = tmp_path / "test.wav"
        audio_file.write_text("audio data")

        result = validate_audio_file_exists(audio_file, Entity.AUDIO_TRACK)

        assert result == audio_file
        assert isinstance(result, Path)

    def test_validate_audio_file_exists_with_string_path(self, tmp_path: Path) -> None:
        """Test validate_audio_file_exists with string path."""
        audio_file = tmp_path / "test.wav"
        audio_file.write_text("audio data")

        result = validate_audio_file_exists(str(audio_file), Entity.VOICE_TRACK)

        assert result == audio_file

    def test_validate_audio_file_exists_none_input(self) -> None:
        """Test validate_audio_file_exists with None input."""
        with pytest.raises(NotProvidedError) as exc_info:
            validate_audio_file_exists(None, Entity.VOCALS_TRACK)

        # Check the error message contains the entity
        error_message = str(exc_info.value)
        assert "vocals track" in error_message

    def test_validate_audio_file_exists_empty_string(self) -> None:
        """Test validate_audio_file_exists with empty string."""
        with pytest.raises(NotProvidedError) as exc_info:
            validate_audio_file_exists("", Entity.SPEECH_TRACK)

        # Check the error message contains the entity
        error_message = str(exc_info.value)
        assert "speech track" in error_message

    def test_validate_audio_file_exists_file_not_found(self, tmp_path: Path) -> None:
        """Test validate_audio_file_exists with non-existent file."""
        nonexistent = tmp_path / "nonexistent.wav"

        with pytest.raises(NotFoundError) as exc_info:
            validate_audio_file_exists(nonexistent, Entity.AUDIO_TRACK)

        error_message = str(exc_info.value)
        assert "Audio track not found" in error_message
        assert str(nonexistent) in error_message

    def test_validate_audio_file_exists_directory_instead_of_file(
        self, tmp_path: Path
    ) -> None:
        """
        Test validate_audio_file_exists when path points to
        directory.
        """
        directory = tmp_path / "audio_dir"
        directory.mkdir()

        with pytest.raises(NotFoundError) as exc_info:
            validate_audio_file_exists(directory, Entity.FILE)

        error_message = str(exc_info.value)
        assert "File not found" in error_message
        assert str(directory) in error_message

    @pytest.mark.parametrize(
        "entity",
        [
            Entity.AUDIO_TRACK,
            Entity.VOICE_TRACK,
            Entity.SPEECH_TRACK,
            Entity.VOCALS_TRACK,
            Entity.FILE,
        ],
    )
    def test_validate_audio_file_exists_different_entities(
        self, tmp_path: Path, entity: AudioFileEntity
    ) -> None:
        """
        Test validate_audio_file_exists with different audio file
        entities.
        """
        audio_file = tmp_path / "test.wav"
        audio_file.write_text("audio data")

        result = validate_audio_file_exists(audio_file, entity)
        assert result == audio_file


class TestValidateAudioDirExists:
    """Test cases for validate_audio_dir_exists function."""

    def test_validate_audio_dir_exists_success(self, tmp_path: Path) -> None:
        """Test validate_audio_dir_exists with existing directory."""
        audio_dir = tmp_path / "audio_files"
        audio_dir.mkdir()

        result = validate_audio_dir_exists(audio_dir, Entity.SONG_DIR)

        assert result == audio_dir
        assert isinstance(result, Path)

    def test_validate_audio_dir_exists_with_string_path(self, tmp_path: Path) -> None:
        """Test validate_audio_dir_exists with string path."""
        audio_dir = tmp_path / "audio_files"
        audio_dir.mkdir()

        result = validate_audio_dir_exists(str(audio_dir), Entity.SONG_DIR)

        assert result == audio_dir

    def test_validate_audio_dir_exists_none_input(self) -> None:
        """
        Test validate_audio_dir_exists with None input for
        SONG_DIR.
        """
        with pytest.raises(NotProvidedError) as exc_info:
            validate_audio_dir_exists(None, Entity.SONG_DIR)

        # Check error message contains the entity name and ui_msg is set
        error_message = str(exc_info.value)
        assert "song directory" in error_message
        assert exc_info.value.ui_msg == UIMessage.NO_SONG_DIR

    def test_validate_audio_dir_exists_none_input_other_entity(self) -> None:
        """
        Test validate_audio_dir_exists with None input for other
        entities.
        """
        with pytest.raises(NotProvidedError) as exc_info:
            validate_audio_dir_exists(None, Entity.DATASET)

        error_message = str(exc_info.value)
        assert "dataset" in error_message
        assert exc_info.value.ui_msg is None

    def test_validate_audio_dir_exists_empty_string(self) -> None:
        """Test validate_audio_dir_exists with empty string."""
        with pytest.raises(NotProvidedError) as exc_info:
            validate_audio_dir_exists("", Entity.SONG_DIR)

        error_message = str(exc_info.value)
        assert "song directory" in error_message

    def test_validate_audio_dir_exists_dir_not_found(self, tmp_path: Path) -> None:
        """
        Test validate_audio_dir_exists with non-existent
        directory.
        """
        nonexistent = tmp_path / "nonexistent_dir"

        with pytest.raises(NotFoundError) as exc_info:
            validate_audio_dir_exists(nonexistent, Entity.DATASET)

        error_message = str(exc_info.value)
        assert "Dataset not found" in error_message
        assert str(nonexistent) in error_message

    def test_validate_audio_dir_exists_file_instead_of_dir(
        self, tmp_path: Path
    ) -> None:
        """Test validate_audio_dir_exists when path points to file."""
        file_path = tmp_path / "audio_file.wav"
        file_path.write_text("audio data")

        with pytest.raises(NotFoundError) as exc_info:
            validate_audio_dir_exists(file_path, Entity.DIRECTORY)

        error_message = str(exc_info.value)
        assert "Directory not found" in error_message
        assert str(file_path) in error_message


class TestValidateModel:
    """Test cases for validate_model function."""

    def test_validate_model_voice_model_exists(
        self, tmp_path: Path, mocker: pytest_mock.MockerFixture
    ) -> None:
        """Test validate_model for existing voice model."""
        model_name = "test_voice_model"
        mock_voice_models_dir = tmp_path / "voice_models"
        mock_voice_models_dir.mkdir()
        model_dir = mock_voice_models_dir / model_name
        model_dir.mkdir()

        mocker.patch("ultimate_rvc.core.common.VOICE_MODELS_DIR", mock_voice_models_dir)

        result = validate_model(model_name, Entity.VOICE_MODEL, mode="exists")

        assert result == model_dir

    def test_validate_model_voice_model_not_exists_success(
        self, tmp_path: Path, mocker: pytest_mock.MockerFixture
    ) -> None:
        """
        Test validate_model for non-existing voice model
        (success case).
        """
        model_name = "new_voice_model"
        mock_voice_models_dir = tmp_path / "voice_models"
        mock_voice_models_dir.mkdir()
        model_dir = mock_voice_models_dir / model_name

        mocker.patch("ultimate_rvc.core.common.VOICE_MODELS_DIR", mock_voice_models_dir)

        result = validate_model(model_name, Entity.VOICE_MODEL, mode="not_exists")

        assert result == model_dir

    def test_validate_model_none_name(self) -> None:
        """Test validate_model with None model name."""
        with pytest.raises(NotProvidedError) as exc_info:
            validate_model(None, Entity.VOICE_MODEL)

        error_message = str(exc_info.value)
        assert "model name" in error_message
        assert exc_info.value.ui_msg == UIMessage.NO_VOICE_MODEL

    def test_validate_model_empty_name(self) -> None:
        """Test validate_model with empty model name."""
        with pytest.raises(NotProvidedError) as exc_info:
            validate_model("", Entity.VOICE_MODEL)

        error_message = str(exc_info.value)
        assert "model name" in error_message

    def test_validate_model_whitespace_name_stripped(
        self, tmp_path: Path, mocker: pytest_mock.MockerFixture
    ) -> None:
        """Test validate_model strips whitespace from model name."""
        model_name = "  test_model  "
        mock_voice_models_dir = tmp_path / "voice_models"
        mock_voice_models_dir.mkdir()
        model_dir = mock_voice_models_dir / "test_model"  # Stripped name
        model_dir.mkdir()

        mocker.patch("ultimate_rvc.core.common.VOICE_MODELS_DIR", mock_voice_models_dir)

        result = validate_model(model_name, Entity.VOICE_MODEL, mode="exists")

        assert result == model_dir

    def test_validate_model_not_found_error(
        self, tmp_path: Path, mocker: pytest_mock.MockerFixture
    ) -> None:
        """
        Test validate_model raises ModelNotFoundError when model
        doesn't exist.
        """
        model_name = "nonexistent_model"
        mock_voice_models_dir = tmp_path / "voice_models"
        mock_voice_models_dir.mkdir()

        mocker.patch("ultimate_rvc.core.common.VOICE_MODELS_DIR", mock_voice_models_dir)

        with pytest.raises(ModelNotFoundError) as exc_info:
            validate_model(model_name, Entity.VOICE_MODEL, mode="exists")

        error_message = str(exc_info.value)
        assert f"Voice model with name '{model_name}' not found" in error_message

    def test_validate_model_exists_error(
        self, tmp_path: Path, mocker: pytest_mock.MockerFixture
    ) -> None:
        """
        Test validate_model raises ModelExistsError when model
        exists but shouldn't.
        """
        model_name = "existing_model"
        mock_voice_models_dir = tmp_path / "voice_models"
        mock_voice_models_dir.mkdir()
        model_dir = mock_voice_models_dir / model_name
        model_dir.mkdir()

        mocker.patch("ultimate_rvc.core.common.VOICE_MODELS_DIR", mock_voice_models_dir)

        with pytest.raises(ModelExistsError) as exc_info:
            validate_model(model_name, Entity.VOICE_MODEL, mode="not_exists")

        error_message = str(exc_info.value)
        assert f"Voice model with name '{model_name}' already exists" in error_message

    @pytest.mark.parametrize(
        ("entity", "expected_ui_msg"),
        [
            (Entity.VOICE_MODEL, UIMessage.NO_VOICE_MODEL),
            (Entity.CUSTOM_EMBEDDER_MODEL, UIMessage.NO_CUSTOM_EMBEDDER_MODEL),
            (Entity.TRAINING_MODEL, None),
            (Entity.CUSTOM_PRETRAINED_MODEL, UIMessage.NO_CUSTOM_PRETRAINED_MODEL),
            (Entity.MODEL, UIMessage.NO_MODEL),
        ],
    )
    def test_validate_model_different_entities(
        self, entity: ModelEntity, expected_ui_msg: UIMessage | None
    ) -> None:
        """Test validate_model with different model entities."""
        with pytest.raises(NotProvidedError) as exc_info:
            validate_model(None, entity)

        error_message = str(exc_info.value)
        assert "model name" in error_message
        assert exc_info.value.ui_msg == expected_ui_msg


class TestValidateUrl:
    """Test cases for validate_url function."""

    def test_validate_url_valid_http(self) -> None:
        """Test validate_url with valid HTTP URL."""
        url = "http://example.com/model.zip"

        # Should not raise any exception
        validate_url(url)

    def test_validate_url_valid_https(self) -> None:
        """Test validate_url with valid HTTPS URL."""
        url = "https://example.com/model.zip"

        # Should not raise any exception
        validate_url(url)

    def test_validate_url_with_path_and_query(self) -> None:
        """Test validate_url with complex URL."""
        url = "https://api.example.com/v1/models/download?id=123&format=zip"

        # Should not raise any exception
        validate_url(url)

    def test_validate_url_empty_string(self) -> None:
        """Test validate_url with empty string."""
        with pytest.raises(NotProvidedError) as exc_info:
            validate_url("")

        error_message = str(exc_info.value)
        assert "URL" in error_message

    def test_validate_url_none_input(self) -> None:
        """Test validate_url with None input."""
        with pytest.raises(NotProvidedError) as exc_info:
            validate_url(None)  # type: ignore[arg-type]

        error_message = str(exc_info.value)
        assert "URL" in error_message

    def test_validate_url_invalid_scheme(self) -> None:
        """Test validate_url with invalid scheme."""
        invalid_url = "ftp://example.com/file.zip"

        with pytest.raises(HttpUrlError) as exc_info:
            validate_url(invalid_url)

        error_message = str(exc_info.value)
        assert "Invalid HTTP-based URL" in error_message
        assert invalid_url in error_message

    def test_validate_url_malformed(self) -> None:
        """Test validate_url with malformed URL."""
        malformed_url = "not-a-url"

        with pytest.raises(HttpUrlError) as exc_info:
            validate_url(malformed_url)

        error_message = str(exc_info.value)
        assert "Invalid HTTP-based URL" in error_message
        assert malformed_url in error_message

    def test_validate_url_missing_protocol(self) -> None:
        """Test validate_url with missing protocol."""
        url_without_protocol = "example.com/model.zip"

        with pytest.raises(HttpUrlError) as exc_info:
            validate_url(url_without_protocol)

        error_message = str(exc_info.value)
        assert "Invalid HTTP-based URL" in error_message
        assert url_without_protocol in error_message

    @pytest.mark.parametrize(
        "valid_url",
        [
            "http://example.com",
            "https://example.com",
            "http://subdomain.example.com/path",
            "https://example.com:8080/api/v1",
            "http://192.168.1.1/file.zip",
            "https://example.com/path?query=value&other=123",
            "http://example.com/path#fragment",
        ],
    )
    def test_validate_url_valid_urls(self, valid_url: str) -> None:
        """Test validate_url with various valid URLs."""
        # Should not raise any exception
        validate_url(valid_url)

    @pytest.mark.parametrize(
        "invalid_url",
        [
            "ftp://example.com",
            "file:///path/to/file",
            "mailto:user@example.com",
            "javascript:alert('xss')",
            "//example.com",  # Protocol-relative
            "example.com",  # Missing protocol
            "http://",  # Incomplete
            "",  # Empty
            "not a url at all",
        ],
    )
    def test_validate_url_invalid_urls(self, invalid_url: str) -> None:
        """Test validate_url with various invalid URLs."""
        with pytest.raises((HttpUrlError, NotProvidedError)):
            validate_url(invalid_url)
