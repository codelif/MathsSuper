from manim import *

class PendulumWithSineGraph(Scene):
    def construct(self):
        # Define pendulum components
        pendulum_pivot = UP * 3.5  # Shift pivot upwards
        pendulum_length = 3
        pendulum_radius = 0.2
        pendulum_angle_amplitude = PI / 6  # max angle (30 degrees)
        omega = 2 * PI / 5  # angular frequency (period = 5 seconds)

        # Time tracking
        self.time_tracker = ValueTracker(0)

        # Pendulum parts
        pivot_dot = Dot(pendulum_pivot, color=WHITE)
        pendulum_line = Line(pendulum_pivot, pendulum_pivot + DOWN * pendulum_length)
        pendulum_ball = Circle(radius=pendulum_radius).move_to(pendulum_line.get_end())
        pendulum_ball.set_fill(RED, opacity=1)

        pendulum_group = VGroup(pendulum_line, pendulum_ball)

        # Create dynamic sine graph
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"include_numbers": True},
        ).to_corner(DOWN + LEFT)

        sine_label = axes.get_axis_labels(x_label="Time (t)", y_label="Amplitude")
        sine_graph = always_redraw(lambda: axes.plot(
            lambda t: np.sin(omega * t),
            x_range=[0, self.time_tracker.get_value()],
            color=BLUE
        ))

        # SHM equation text
        shm_eq = MathTex(r"\frac{d^2\theta}{dt^2} + \omega^2 \theta = 0")
        shm_eq.to_corner(UP + RIGHT)

        # Pendulum motion updater
        def update_pendulum(group):
            time = self.time_tracker.get_value()
            angle = pendulum_angle_amplitude * np.sin(omega * time)
            pendulum_line.put_start_and_end_on(
                pendulum_pivot,
                pendulum_pivot + pendulum_length * np.array([np.sin(angle), -np.cos(angle), 0])
            )
            pendulum_ball.move_to(pendulum_line.get_end())

        pendulum_group.add_updater(update_pendulum)

        # Add components to the scene
        self.add(pivot_dot, pendulum_group, axes, sine_label, shm_eq, sine_graph)

        # Animate the time tracker and the scene
        self.play(self.time_tracker.animate.set_value(10), run_time=10, rate_func=linear)

        # Stop pendulum motion after the animation
        pendulum_group.remove_updater(update_pendulum)
