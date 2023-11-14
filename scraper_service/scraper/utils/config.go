package utils

type Config struct {
	RedisHost        string
	RedisPort        string
	PostgresHost     string
	PostgresPort     string
	PostgresUser     string
	PostgresPassword string
	PostgresDatabase string
}

func LoadConfig() Config {
	return Config{
		RedisHost:        GetEnv("REDIS_HOST", "localhost"),
		RedisPort:        GetEnv("REDIS_PORT", "6379"),
		PostgresHost:     GetEnv("POSTGRES_HOST", "localhost"),
		PostgresPort:     GetEnv("POSTGRES_PORT", "5432"),
		PostgresUser:     GetEnv("POSTGRES_USER", "postgres"),
		PostgresPassword: GetEnv("POSTGRES_PASSWORD", "postgres"),
		PostgresDatabase: GetEnv("POSTGRES_DB", "postgres"),
	}
}
