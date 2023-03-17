class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вывести строку сообщения о проведенной тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000  # перевод из метров в километры
    LEN_STEP: float = 0.65  # расстояние одного шага в метрах
    MIN_IN_HOUR: int = 60  # перевод часы в минуты

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type: str = self.__class__.__name__
        duration: float = self.duration
        distance: float = self.get_distance()
        speed: float = self.get_mean_speed()
        calories: float = self.get_spent_calories()
        return InfoMessage(training_type, duration, distance, speed, calories)


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18  # коэффициент для расчета ккал
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79  # коэффициент для расчета ккал

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight / self.M_IN_KM * self.duration
                           * self.MIN_IN_HOUR)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER_1: float = 0.035  # коэффициент для расчета ккал
    CALORIES_WEIGHT_MULTIPLIER_2: float = 0.029  # коэффициент для расчета ккал
    KMH_TO_MS: float = 0.278  # перевод скорости из км/ч в м/с
    HEIGHT_TO_METERS: int = 100  # перевод роста из сантиметров в метры

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)

        self.height = height / self.HEIGHT_TO_METERS

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        speed_in_ms: float = self.get_mean_speed() * self.KMH_TO_MS

        calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER_1 * self.weight
                           + (speed_in_ms**2 / self.height)
                           * self.CALORIES_WEIGHT_MULTIPLIER_2
                           * self.weight)
                           * self.duration * self.MIN_IN_HOUR)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_MEANS_SPEED_MULTIPLIER: int = 2  # коэффициент для расчета ккал
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1  # коэффициент для расчета ккал
    LEN_STEP: float = 1.38  # расстояние одного гребка в метрах

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плавании."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        calories: float = ((self.get_mean_speed()
                           + self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.CALORIES_MEANS_SPEED_MULTIPLIER
                           * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_classes: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    action, duration, weight, *other = data

    if workout_type in training_classes:
        return training_classes[workout_type](action, duration, weight, *other)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
