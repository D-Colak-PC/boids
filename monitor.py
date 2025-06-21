from time import perf_counter
from collections import deque
from functools import wraps
from consts import FPS, PERFORMANCE_MONITORING


def monitor_method(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not PERFORMANCE_MONITORING:
            return None
        return func(self, *args, **kwargs)

    return wrapper


class PerformanceMonitor:
    def __init__(self):
        self.frame_times = deque(maxlen=FPS)
        self.simulation_times = deque(maxlen=FPS)
        self.rendering_times = deque(maxlen=FPS)

        self.frame_start_time: float = None
        self.simulation_start_time: float = None
        self.rendering_start_time: float = None
        self.frames = 0
        self.start_time = perf_counter()

    @monitor_method
    def start_frame(self) -> None:
        self.frame_start_time = perf_counter()

    @monitor_method
    def start_simulation(self) -> None:
        self.simulation_start_time = perf_counter()

    @monitor_method
    def end_simulation(self) -> None:
        if self.simulation_start_time is not None:
            sim_time = perf_counter() - self.simulation_start_time
            self.simulation_times.append(sim_time * 1000)

    @monitor_method
    def start_rendering(self) -> None:
        self.rendering_start_time = perf_counter()

    @monitor_method
    def end_rendering(self) -> None:
        if self.rendering_start_time is not None:
            render_time = perf_counter() - self.rendering_start_time
            self.rendering_times.append(render_time * 1000)

    @monitor_method
    def end_frame(self) -> None:
        if self.frame_start_time is not None:
            frame_time = perf_counter() - self.frame_start_time
            self.frame_times.append(frame_time * 1000)
            self.frames += 1

    @monitor_method
    def get_fps(self) -> float:
        if not self.frame_times:
            return 0.0
        avg_frame_time = self.get_average_frame_time()
        return 1000.0 / avg_frame_time if avg_frame_time > 0 else 0.0

    @monitor_method
    def get_average_frame_time(self) -> float:
        if not self.frame_times:
            return 0.0
        return sum(self.frame_times) / len(self.frame_times)

    @monitor_method
    def get_average_simulation_time(self) -> float:
        if not self.simulation_times:
            return 0.0
        return sum(self.simulation_times) / len(self.simulation_times)

    @monitor_method
    def get_average_rendering_time(self) -> float:
        if not self.rendering_times:
            return 0.0
        return sum(self.rendering_times) / len(self.rendering_times)

    @monitor_method
    def get_overall_fps(self) -> float:
        elapsed = perf_counter() - self.start_time
        return self.frames / elapsed if elapsed > 0 else 0.0

    @monitor_method
    def print_performance(self) -> None:
        summary = (
            f"FPS: {self.get_fps():.1f} \t"
            f"Frame: {self.get_average_frame_time():.2f}ms \t\t"
            f"Sim: {self.get_average_simulation_time():.2f}ms \t\t"
            f"Render: {self.get_average_rendering_time():.2f}ms \t\t"
            f"Overall FPS: {self.get_overall_fps():.1f}"
        )

        print(summary)
