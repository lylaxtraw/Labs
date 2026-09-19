"""Pruebas unitarias para el módulo de animaciones."""

import pytest
from src.lib.animation import AnimationScene, get_scene, SCENES


class TestAnimationScene:
    """Pruebas para la clase AnimationScene."""

    def test_scene_creation(self):
        """Verifica la creación correcta de una escena."""
        frames = [lambda d, fn: None for _ in range(3)]
        scene = AnimationScene("Test Scene", frames)

        assert scene.name == "Test Scene"
        assert scene.frame_count == 3

    def test_get_frame_returns_callable(self):
        """Verifica que get_frame retorna una función."""
        frame = lambda d, fn: None
        scene = AnimationScene("Test", [frame, frame, frame])

        result = scene.get_frame(0)
        assert callable(result)

    def test_get_frame_cycles_correctly(self):
        """Verifica que get_frame cicla correctamente."""
        frame1 = lambda d, fn: 1
        frame2 = lambda d, fn: 2
        frame3 = lambda d, fn: 3
        scene = AnimationScene("Test", [frame1, frame2, frame3])

        # Verificar que los índices válidos funcionan
        assert scene.get_frame(0) is frame1
        assert scene.get_frame(1) is frame2
        assert scene.get_frame(2) is frame3

        # Verificar que los índices fuera de rango se ciclan
        assert scene.get_frame(3) is frame1
        assert scene.get_frame(4) is frame2


class TestScenesAvailability:
    """Pruebas para verificar que las escenas están disponibles."""

    def test_scenes_list_has_four_scenes(self):
        """Verifica que SCENES contenga 4 escenas."""
        assert len(SCENES) == 4

    def test_all_scenes_have_names(self):
        """Verifica que todas las escenas tengan nombres."""
        for scene in SCENES:
            assert isinstance(scene.name, str)
            assert len(scene.name) > 0

    def test_all_scenes_have_frames(self):
        """Verifica que todas las escenas tengan frames."""
        for scene in SCENES:
            assert scene.frame_count > 0
            for i in range(scene.frame_count):
                frame = scene.get_frame(i)
                assert callable(frame)

    def test_get_scene_returns_correct_scene(self):
        """Verifica que get_scene retorna la escena correcta."""
        scene0 = get_scene(0)
        scene1 = get_scene(1)
        scene2 = get_scene(2)
        scene3 = get_scene(3)

        assert scene0 is SCENES[0]
        assert scene1 is SCENES[1]
        assert scene2 is SCENES[2]
        assert scene3 is SCENES[3]

    def test_get_scene_cycles_with_invalid_index(self):
        """Verifica que get_scene cicla con índices fuera de rango."""
        scene4 = get_scene(4)
        scene5 = get_scene(5)

        assert scene4 is SCENES[0]
        assert scene5 is SCENES[1]


class TestSceneNames:
    """Pruebas para verificar los nombres específicos de las escenas."""

    def test_scene_1_is_circles(self):
        """Verifica que la escena 1 sea Círculos Animados."""
        assert "Círculo" in SCENES[0].name or "circulo" in SCENES[0].name.lower()

    def test_scene_2_is_lines(self):
        """Verifica que la escena 2 sea Líneas Dinámicas."""
        assert "Línea" in SCENES[1].name or "linea" in SCENES[1].name.lower()

    def test_scene_3_is_rectangles(self):
        """Verifica que la escena 3 sea Rectángulos Rotantes."""
        assert "Rectángulo" in SCENES[2].name or "rectangulo" in SCENES[2].name.lower()

    def test_scene_4_is_pattern(self):
        """Verifica que la escena 4 sea Patrón Parpadeante."""
        assert "Patrón" in SCENES[3].name or "patron" in SCENES[3].name.lower()
